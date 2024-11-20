# Conversation Thread

[35mTime: 2024-11-18 16:51:53
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
[34mTime: 2024-11-18 16:51:54
Role: assistant
Content: ### Code Review Summary

#### Correctness and Functionality
**Score: 9/10**  
**Explanation:** The code appears to correctly log HTTP requests and responses, handle exceptions, and manages payloads effectively. However, the logging of content (especially potentially sensitive data) requires careful consideration to ensure it meets privacy and data handling guidelines.  
**Improvement Suggestion:** Review the handling of request and response bodies to ensure that sensitive data is not logged unintentionally.

#### Code Quality and Maintainability
**Score: 8/10**  
**Explanation:** The code is reasonably well-structured with clear organization and naming conventions. However, some methods could be simplified or refactored for better readability and maintainability.  
**Improvement Suggestion:** Breaking down the `InvokeAsync` method into smaller, well-defined methods would enhance clarity and make unit testing easier.

#### Performance and Efficiency
**Score: 7/10**  
**Explanation:** The use of memory streams and reading request bodies could lead to performance bottlenecks, especially for large requests. The buffering and copying processes in `InvokeAsync` might have room for optimization.  
**Improvement Suggestion:** Consider streaming the request body directly or using a different approach to handle large payloads to improve performance.

#### Security and Vulnerability Assessment
**Score: 7/10**  
**Explanation:** The code does well in logging but might expose sensitive information in logs. The response payload handling could lead to information leakage if not managed properly.  
**Improvement Suggestion:** Implement stricter filtering of request and response content that is logged to avoid exposure of sensitive data.

#### Code Consistency and Style
**Score: 9/10**  
**Explanation:** The code adheres to a consistent coding style, which promotes readability. Naming conventions are clear and consistent throughout.  
**Improvement Suggestion:** While the overall style is good, consider adhering to a style guide for ASP.NET Core applications for even better consistency, especially concerning standard practices and patterns.

#### Scalability and Extensibility
**Score: 6/10**  
**Explanation:** While the middleware is functional, the design does not clearly separate concerns, which could hinder scalability and extensibility as more features are added in the future.  
**Improvement Suggestion:** Introduce dependency injection and separation of concerns to allow for easier expansion and modification in the future.

#### Error Handling and Robustness
**Score: 8/10**  
**Explanation:** The error handling is mostly robust, with various exceptions handled adequately. However, there is some complexity in the exception handling that could lead to unhandled exceptions.  
**Improvement Suggestion:** Simplify the exception handling logic and ensure that all possible exceptions are accounted for and handled uniformly.

### Overall Score: 7.57/10

### Code Improvement Summary:
1. **Sensitive Data Handling:** Review and refactor logging to ensure sensitive information is not inadvertently logged.
2. **Method Decomposition:** Refactor the `InvokeAsync` method into smaller methods to enhance readability and maintainability.
3. **Performance Optimization:** Consider strategies to streamline request body handling to avoid bottlenecks with large payloads.
4. **Security Improvements:** Implement content filtering in logs to protect sensitive data from being exposed.
5. **Separation of Concerns:** Utilize dependency injection principles and consider restructuring the code to improve scalability and extensibility.
6. **Error Handling Simplicity:** Simplify exception handling to improve clarity and ensure all exceptions are managed appropriately.[0m
==================================================
