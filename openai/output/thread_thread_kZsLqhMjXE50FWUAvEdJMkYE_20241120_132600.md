# Conversation Thread

[35mTime: 2024-11-18 16:19:44
Role: user
Content: using System.Diagnostics;
using System.Net;
using System.Text;
using System.Text.Json;
using Microsoft.AspNetCore.Http;
using Serilog;
using Serilog.Events;
using OTC.Exceptions;
using OTC.ErrorsStandardModel;


namespace OTC.Middleware;

public class LogHttpMiddleware
{
    const string MessageTemplate =
        "{@duration} {@traceId} {@url} {@method} {@request_headers} {@request_body} {@response_status} {@response_headers} {@response_body}";

    static readonly ILogger Log = Serilog.Log.ForContext<LogHttpMiddleware>();
    readonly RequestDelegate _next;
    private static readonly string[] _documentsFilePath = ["documents", "sales-orders/receipt", "billings"];

    public LogHttpMiddleware(
        RequestDelegate next
    )
    {
        if (next == null) throw new ArgumentNullException(nameof(next));
        _next = next;
    }

    public async Task InvokeAsync(HttpContext httpContext)
    {
        if (httpContext == null) throw new ArgumentNullException(nameof(httpContext));
        var request = httpContext.Request;
        request.EnableBuffering();
        var buffer = new byte[Convert.ToInt32(request.ContentLength)];
        await request.Body.ReadAsync(buffer, 0, buffer.Length);
        var requestContent = Encoding.UTF8.GetString(buffer);
        request.Body.Position = 0;
        var options = new JsonSerializerOptions
        {
            PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
            WriteIndented = true
        };

        var sw = Stopwatch.StartNew();
        var bodyStream = httpContext.Response.Body;
        var memoryStream = new MemoryStream();
        string payloadError = string.Empty;

        try
        {
            if (!_documentsFilePath.Any(httpContext.Request.Path.ToString().Contains))
            {
                httpContext.Response.Body = memoryStream;
            }

            await _next(httpContext);
            sw.Stop();

            var statusCode = httpContext.Response?.StatusCode;
            var level = statusCode > 499 ? LogEventLevel.Error : LogEventLevel.Information;
            var logHttpMessage = LogHttpMessage.SetLog(httpContext, sw.Elapsed.TotalMilliseconds);
            string? logBody = await GetBodyHttpContext(httpContext, memoryStream, bodyStream);

            Console.WriteLine($"Trace id: {logHttpMessage.traceId}");
            Log.Write(
                level,
                MessageTemplate,
                logHttpMessage.duration,
                logHttpMessage.traceId,
                logHttpMessage.request?.endpoint,
                logHttpMessage.request?.method,
                logHttpMessage.request?.header,
                requestContent,
                logHttpMessage.response?.status,
                logHttpMessage.response?.header,
                logBody
            );
        }
        catch (BadRequestException badRequestEx)
        {
            await WriteLogError(badRequestEx, requestContent, (int)HttpStatusCode.BadRequest, httpContext, sw);
            payloadError = JsonSerializer.Serialize(badRequestEx.ResponseError, options);
        }
        catch (InternalErrorException internalErrorEx)
        {
            await WriteLogError(internalErrorEx, requestContent, (int)HttpStatusCode.InternalServerError, httpContext,
                sw);
            payloadError = JsonSerializer.Serialize(internalErrorEx.ResponseError, options);
        }
        catch (Exception ex)
        {
            await WriteLogError(ex, requestContent, (int)HttpStatusCode.InternalServerError, httpContext, sw);
            var st = new StackTrace(ex, true);
            var internalErrors = st.GetFrames()
                .Select(frame =>
                {
                    return new InternalError
                    {
                        Message = ex.Message,
                        CallerFilePath = frame.GetFileName(),
                        CallerMemberName = frame.GetMethod().DeclaringType.Name,
                        CallerLineNo = frame.GetFileLineNumber()
                    };
                }).FirstOrDefault();
            var baseResponseError = new BaseResponseError<InternalError>
            {
                Type = "https://tools.ietf.org/html/rfc7231#section-6.5.1",
                Title = "Internal Server Error",
                Status = (int)HttpStatusCode.InternalServerError,
                Errors = internalErrors,
                TraceId = httpContext.TraceIdentifier
            };
            payloadError = JsonSerializer.Serialize(baseResponseError, options);
        }
        finally
        {
            if (!string.IsNullOrEmpty(payloadError))
            {
                await SetPayloadToResponseMemoryStream(payloadError, memoryStream, httpContext, bodyStream);
            }

            memoryStream.Dispose();
        }
    }

    private async Task WriteLogError(Exception exception, string requestContent, int statusCode,
        HttpContext httpContext,
        Stopwatch sw)
    {
        httpContext.Response.ContentType = "application/json";
        httpContext.Response.StatusCode = statusCode;
        var logHttpMessage = LogHttpMessage.SetLog(httpContext, sw.Elapsed.TotalMilliseconds);
        Console.WriteLine($"Trace id: {logHttpMessage.traceId}");
        Log.Error(
            exception,
            MessageTemplate,
            logHttpMessage.duration,
            logHttpMessage.traceId,
            logHttpMessage.request?.endpoint,
            logHttpMessage.request?.method,
            logHttpMessage.request?.header,
            requestContent,
            logHttpMessage.response?.status,
            logHttpMessage.response?.header
        );
    }

    private async Task<string> GetBodyHttpContext(HttpContext httpContext, MemoryStream memoryStream, Stream bodyStream)
    {
        if (httpContext.Response?.ContentType != "application/pdf")
        {
            memoryStream.Seek(0, SeekOrigin.Begin);
            var responseBody = await new StreamReader(memoryStream).ReadToEndAsync();
            memoryStream.Seek(0, SeekOrigin.Begin);
            await memoryStream.CopyToAsync(bodyStream);
            return responseBody;
        }

        return null;
    }

    private async Task SetPayloadToResponseMemoryStream(string payload, MemoryStream memoryStream,
        HttpContext httpContext, Stream? bodyStream)
    {
        var writer = new StreamWriter(memoryStream);
        await writer.WriteAsync(payload);
        await writer.FlushAsync();
        memoryStream.Seek(0, SeekOrigin.Begin);
        await memoryStream.CopyToAsync(bodyStream);
        await httpContext.Response.WriteAsync(payload);
    }
}[0m
==================================================
[34mTime: 2024-11-18 16:19:46
Role: assistant
Content: Here is the review of the provided C# middleware code:

### Code Review Summary

#### Correctness and Functionality
**Score: 9/10**  
Explanation: The middleware implements logging for HTTP requests and responses correctly. It includes proper error handling for different exceptions and logs relevant HTTP data accurately. The logic appears to be sound; however, minor improvements in performance and handling of edge cases could enhance functionality further.

**Improvement Suggestion:** Ensure that edge cases such as very large payloads or unsupported content types are handled gracefully without causing timeouts or memory issues.

#### Code Quality and Maintainability
**Score: 8/10**  
Explanation: The code is mostly clean and adheres to principles of object-oriented design. It is well-structured, with clear separation of concerns. However, the use of hard-coded values (like the document file paths) and nested try-catch statements can make maintenance challenging.

**Improvement Suggestion:** Consider moving constants to configuration settings or a separate class to avoid magic strings and improve maintainability.

#### Performance and Efficiency
**Score: 7/10**  
Explanation: The middleware handles requests efficiently but reads the entire body into memory, which can lead to performance issues with large requests. The `request.EnableBuffering` method is used excessively in cases where body content is not needed.

**Improvement Suggestion:** Implement a more efficient reading strategy, perhaps by only buffering necessary request data and streamlining the response memory handling.

#### Security and Vulnerability Assessment
**Score: 8/10**  
Explanation: The code demonstrates awareness of security through exception handling and accurately setting response status codes. However, potential vulnerabilities, like logging of sensitive information in request bodies, could pose risks.

**Improvement Suggestion:** Ensure that sensitive request body contents, such as passwords or personal data, are filtered out from the logs before being written.

#### Code Consistency and Style
**Score: 9/10**  
Explanation: The code generally adheres to consistent naming conventions and indentation. The use of comments and structured organization helps maintain readability.

**Improvement Suggestion:** Add more inline comments to particularly complex sections to enhance clarity. Also, use consistent formatting for lambda expressions and method parameters.

#### Scalability and Extensibility
**Score: 7/10**  
Explanation: The design supports logging middleware extensibility, but it lacks modularity. The use of hard-coded endpoints makes modifying logging behavior more difficult.

**Improvement Suggestion:** Consider implementing dependency injection for configurable settings, like file paths, and separate the logging mechanism into a dedicated service for enhanced flexibility.

#### Error Handling and Robustness
**Score: 8/10**  
Explanation: The middleware includes robust error handling with specific exceptions captured. However, its current design may still allow for uncaught exceptions in certain scenarios.

**Improvement Suggestion:** Implement a fallback logging mechanism for exceptions that are not specifically caught to improve robustness.

### Overall Score
**Overall Score: 7.71/10**

### Code Improvement Summary:
1. **Edge Case Handling:** Review and optimize the error handling to accommodate large payloads and unsupported content types.
2. **Configuration Management:** Move hard-coded strings and values to a configuration file for better maintainability.
3. **Performance Optimization:** Streamline the reading and response handling to improve performance with large requests.
4. **Security Enhancements:** Filter out sensitive information in logs to mitigate security risks.
5. **Dependency Injection:** Use dependency injection to manage configurable settings for file paths and other constants.
6. **Fallback Mechanism for Errors:** Implement a mechanism for logging uncaught errors to enhance robustness.[0m
==================================================
