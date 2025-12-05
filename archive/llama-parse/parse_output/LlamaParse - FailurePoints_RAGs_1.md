#

# Seven Failure Points When Engineering a Retrieval Augmented Generation System

# Seven Failure Points When Engineering a Retrieval Augmented Generation System

Authors: Scott Barnett, Stefanus Kurniawan, Srikanth Thudumu, Zach Brannelly, Mohamed Abdelrazek

Emails: {scott.barnett,stefanus.kurniawan,srikanth.thudumu,zach.brannelly,mohamed.abdelrazek}@deakin.edu.au

Affiliation: Applied Artificial Intelligence Institute, Geelong, Australia

# Abstract

Software engineers are increasingly adding semantic search capabilities to applications using a strategy known as Retrieval Augmented Generation (RAG). A RAG system involves finding documents that semantically match a query and then passing the documents to a large language model (LLM) such as ChatGPT to extract the right answer using an LLM. RAG systems aim to reduce hallucinated responses from LLMs, link sources/references to generated responses, and remove the need for annotating documents with meta-data. This paper presents an experience report on the failure points of RAG systems from three case studies in research, education, and biomedical domains. The key takeaways include the validation of a RAG system being feasible during operation and the evolution of the robustness of a RAG system rather than being designed at the start. The paper concludes with potential research directions on RAG systems for the software engineering community.

# CCS Concepts

- Software and its engineering → Empirical software validation

# Keywords

Retrieval Augmented Generation, RAG, SE4AI, Case Study

# Introduction

The new advancements of Large Language Models (LLMs), including ChatGPT, have given software engineers new capabilities to build new HCI solutions, complete complex tasks, summarize documents, answer questions, and generate new content. However, LLMs have limitations when it comes to up-to-date or domain-specific knowledge. This paper focuses on Retrieval-Augmented Generation (RAG) systems as a solution to this challenge by integrating retrieval mechanisms with the generative capabilities of LLMs.

# Research Questions

- What are the failure points that occur when engineering a RAG system?

# Research Findings

The paper presents an empirical experiment using the BioASQ dataset to report on potential failure points. The experiment involved 15,000 documents and 1000 questions.

# Reference

Scott Barnett, Stefanus Kurniawan, Srikanth Thudumu, Zach Brannelly, Mohamed Abdelrazek. 2024. Seven Failure Points When Engineering a Retrieval Augmented Generation System. In Proceedings of 3rd International Conference on AI Engineering — Software Engineering for AI (CAIN 2024). ACM, New York, NY, USA, 6 pages. DOI Link
---
#
# CAIN 2024 Presentation

# CAIN 2024, April 2024, Lisbon, Portugal

# Presenters: Scott Barnett, Stefanus Kurniawan, Srikanth Thudumu, Zach Brannelly, Mohamed Abdelrazek

# Key Considerations in Engineering a RAG System:

We indexed all documents and ran the system to generate question and answer pairs. The responses were stored using GPT-4. Validation was done with OpenAI evals. Manual inspection was conducted to identify patterns.

- Catalogue of failure points in RAG systems
- Experience report from 3 case studies of implementing a RAG system
- Research direction for RAG systems based on lessons learned

# Contributions:

- Catalogue of failure points (FP) in RAG systems
- Experience report from 3 case studies of implementing a RAG system
- Research direction for RAG systems based on lessons learned

# Related Work

Retrieval augmented generation involves using documents to augment large language models through pre-training and at inference time. Challenges arise when using large language models for information extraction.

Large language models are used across the RAG pipeline including retriever, data generation, rewriter, and reader.

Errors and failures in RAG systems overlap with other information retrieval systems.

# Retrieval Augmented Generation

RAG works by converting a natural language query into an embedding to search documents and generate answers using a large language model.

# Index Process

In a RAG system, documents are split into smaller chunks and converted into embeddings during the Index process. Design decisions include chunk size and embedding strategy.

# Query Process

The Query process involves converting a natural language question into a general query, calculating an embedding, retrieving relevant documents, and re-ranking them to locate the answer.

Software engineers need to consider tradeoffs in chunking, token limits, and rate limits when designing a RAG system.

Sources: OpenAI Evals, ChatGPT2, Claude, Bard
---
#
# Seven Failure Points When Engineering a Retrieval Augmented Generation System

# Seven Failure Points When Engineering a Retrieval Augmented Generation System

CAIN 2024, April 2024, Lisbon, Portugal

# Index Process

Process
Failure point
Data flow

Chunker
Missing Content
Text input/output

Database
Processing stage
Incorrect Specificity

Query Process
Not Processed
Response Not Extracted

# Figure 1: Indexing and Query processes required for creating a Retrieval Augmented Generation (RAG) system.

The indexing process is typically done at development time and queries at runtime. Failure points identified in this study are shown in red boxes. All required stages are underlined. Figure expanded from [19].

# Final Stage of RAG Pipeline

The final stage of a RAG pipeline is when the answer is extracted from the generated text. Readers are responsible for filtering the noise from the prompt, adhering to formatting instructions, and producing the output to return for the query.

# Implementation of RAG Systems

Implementation of a RAG system requires customizing multiple prompts to process questions and answers. This process ensures that questions relevant for the domain are returned.

# Case Studies

# 4.1 Cognitive Reviewer

Cognitive Reviewer is a RAG system designed to support researchers in analyzing scientific documents. It does the Index process at run time and relies on a robust data processing pipeline to handle uploaded documents.

# 4.2 AI Tutor

The AI Tutor is a RAG system where students ask questions about the unit and answers are sourced from the learning content. It integrates into Deakin’s learning management system and includes a rewriter to generalize queries.

# 4.3 Biomedical Question and Answer

A RAG system was created using the BioASQ dataset comprised of questions, links to documents, and answers. The dataset contains domain-specific question and answer pairs.

All scripts, data, and examples of each of the failure points for the BioASQ case study are available online here.
---
#

# RAG Case Studies Summary

# RAG Case Studies Summary

# Case Studies Overview

Case Study
Domain
Doc Types
Dataset Size
RAG Stages
Sample Questions

Cognitive Reviewer*
Research
PDFs
(Any size)
Chunker, Rewriter, Retriever, Reader
What are the key points covered in this paper?

AI Tutor*
Education
Videos, HTML, PDF
38
Chunker, Rewriter, Retriever, Reader
What were the topics covered in week 6?

BioASQ
Biomedical
Scientific PDFs
4017
Chunker, Retriever, Reader
Define pseudotumor cerebri. How is it treated?

*Case studies marked with a * are running systems currently in use.

# Failure Points of RAG Systems

From the case studies, the following failure points were identified:

1. Missing Content: Questions without answers in available documents.
2. Missed the Top Ranked Documents: Answers present but not highly ranked.
3. Not in Context - Consolidation strategy Limitations: Answers not included in the context.
4. Not Extracted: Answers present but not extracted correctly.
5. Wrong Format: Incorrect format extraction.
6. Incorrect Specificity: Answers not specific enough or too specific.

# Lessons and Future Research Directions

The lessons learned from the case studies are summarized in Table 2. Key considerations for engineering a RAG system include:

- Chunking and Embeddings: Research on chunking techniques and their impact on retrieval processes.
- RAG vs Finetuning: Comparison of finetuning and RAG for customizing large language models.

Further research is needed to address the identified failure points and enhance the performance of RAG systems.
---
#

# Seven Failure Points When Engineering a Retrieval Augmented Generation System

# Seven Failure Points When Engineering a Retrieval Augmented Generation System

CAIN 2024, April 2024, Lisbon, Portugal

FP
Lesson
Description
Case Studies

FP4
Larger context get better results
A larger context enabled more accurate responses (8K vs 4K). Contrary to prior work with GPT-3.5.
AI Tutor

FP1
Semantic caching drives cost and latency down
RAG systems struggle with concurrent users due to rate limits and the cost of LLMs. Prepopulate the semantic cache with frequently asked questions.
AI Tutor

FP5-7
Jailbreaks bypass the RAG system and hit the safety training
Research suggests fine-tuning LLMs reverses safety training, test all fine-tuned LLMs for RAG system.
AI Tutor

FP2, FP4
Adding meta-data improves retrieval
Adding the file name and chunk number into the retrieved context helped the reader extract the required information. Useful for chat dialogue.
AI Tutor

FP2, FP4-7
Open source embedding models perform better for small text
Opensource sentence embedding models performed as well as closed source alternatives on small text.
BioASQ, AI Tutor

FP2-7
RAG systems require continuous calibration
RAG systems receive unknown input at runtime requiring constant monitoring.
AI Tutor, BioASQ

FP1, FP2
Implement a RAG pipeline for configuration
A RAG system requires calibrating chunk size, embedding strategy, chunking strategy, retrieval strategy, consolidation strategy, context size, and prompts.
Cognitive Reviewer, AI Tutor, BioASQ

FP2, FP4
RAG pipelines created by assembling bespoke solutions are suboptimal
End-to-end training enhances domain adaptation in RAG systems.
BioASQ, AI Tutor

FP2-7
Testing performance characteristics are only possible at runtime
Offline evaluation techniques such as G-Evals look promising but are premised on having access to labelled question and answer pairs.
Cognitive Reviewer, AI Tutor

Table 2: The lessons learned from the three case studies with key takeaways for future RAG implementations

Security/Privacy Considerations: It is important to sort out the security/privacy concerns regarding who can access what. Additionally, as the foundation model evolves or new data is added, finetuning needs to be rerun. RAG systems offer a pragmatic solution for updating knowledge with new documents and controlling user access to chunks.

# Testing and Monitoring RAG systems

Software engineering best practices are still emerging for RAG systems. Test data availability and quality metrics are crucial for making quality tradeoffs. Realistic domain relevant questions and answers generation remains an open problem.

Quality metrics are essential for assisting engineers in making quality tradeoffs. Large language models introduce latency concerns and performance characteristics that change with each new release.

Adaptations for machine learning systems have yet to be applied to LLM based systems like RAGs. Incorporating ideas from self-adaptive systems for monitoring and adapting RAG systems is a potential area for further exploration.

# Conclusion

RAG systems leverage LLMs for information retrieval. This paper presents lessons learned from case studies and provides guidance for practitioners on challenges faced when implementing RAG systems. Future research directions include chunking and embeddings, RAG vs Finetuning, and Testing and Monitoring.

# Acknowledgments

Special thanks to Amanda Edgar, Rajesh Vasa, Kon Mouzakis, Matteo Vergani, Trish McCluskey, Kathryn Perus, Tara Draper, Joan Sutherland, and Ruary Ross for their support and involvement in the AI Tutor project.
---
#

# CAIN 2024 Conference References

# CAIN 2024 Conference References

# References:

1. Fu Bang. 2023. GPTCache: An Open-Source Semantic Cache for LLM Applications. Enabling Faster Answers and Cost Savings. In 3rd Workshop for Natural Language Processing Open Source Software.
2. Maria Casimiro, Paolo Romano, David Garlan, Gabriel Moreno, Eunsuk Kang, and Mark Klein. 2022. Self-adaptive Machine Learning Systems: Research Challenges and Opportunities. 133–155. Link
3. Jiawei Chen, Hongyu Lin, Xianpei Han, and Le Sun. 2023. Benchmarking Large Language Models in Retrieval-Augmented Generation. arXiv preprint arXiv:2309.01431 (2023).
4. Mingda Chen, Xilun Chen, and Wen-tau Yih. 2023. Efficient Open Domain Multi-Hop Question Answering with Few-Shot Data Synthesis. arXiv preprint arXiv:2305.13691 (2023).
5. Alex Cummaudo, Scott Barnett, Rajesh Vasa, and John Grundy. 2020. Threshy: Supporting safe usage of intelligent web services. In Proceedings of the 28th ACM Joint Meeting on European Software Engineering Conference and Symposium on the Foundations of Software Engineering. 1645–1649.
6. Alex Cummaudo, Scott Barnett, Rajesh Vasa, John Grundy, and Mohamed Abdelrazek. 2020. Beware the evolving ‘intelligent’ web service! An integration architecture tactic to guard AI-first components. In Proceedings of the 28th ACM Joint Meeting on European Software Engineering Conference and Symposium on the Foundations of Software Engineering. 269–280.
7. Kelvin Guu, Kenton Lee, Zora Tung, Panupong Pasupat, and Mingwei Chang. 2020. Retrieval augmented language model pre-training. In International conference on machine learning. PMLR, 3929–3938.
8. Sebastian Hofstätter, Jiecao Chen, Karthik Raman, and Hamed Zamani. 2023. Fid-light: Efficient and effective retrieval-augmented text generation. In Proceedings of the 46th International ACM SIGIR Conference on Research and Development in Information Retrieval. 1437–1447.
9. Gautier Izacard and Edouard Grave. 2020. Leveraging passage retrieval with generative models for open domain question answering. arXiv preprint

# Additional References:

- Anastasia Krithara, Anastasios Nentidis, Konstantinos Bougiatiotis, and Georgios Paliouras. 2023. BioASQ-QA: A manually curated corpus for biomedical question answering. Scientific Data 10 (2023), 170. Citation Key: 422.
- Simon Lermen, Charlie Rogers-Smith, and Jeffrey Ladish. 2023. LoRA Fine-tuning Efficiently Undoes Safety Training in Llama 2-Chat 70B. arXiv:2310.20624 [cs.LG]
- Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, et al. 2020. Retrieval-augmented generation for knowledge-intensive nlp tasks. Advances in Neural Information Processing Systems 33 (2020), 9459–9474.
- Nelson F Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, and Percy Liang. 2023. Lost in the middle: How language models use long contexts. arXiv preprint arXiv:2307.03172 (2023).
- Yang Liu, Dan Iter, Yichong Xu, Shuohang Wang, Ruochen Xu, and Chenguang Zhu. 2023. G-eval: Nlg evaluation using gpt-4 with better human alignment, may 2023. arXiv preprint arXiv:2303.16634 (2023).
- Noor Nashid, Mifta Sintaha, and Ali Mesbah. 2023. Retrieval-based prompt selection for code-related few-shot learning. In Proceedings of the 45th International Conference on Software Engineering (ICSE’23).
- OpenAI. 2023. GPT-4 Technical Report. Link
- Alec Radford, Jong Wook Kim, Tao Xu, Greg Brockman, Christine McLeavey, and Ilya Sutskever. 2023. Robust speech recognition via large-scale weak supervision. In International Conference on Machine Learning. PMLR, 28492–28518.
- Shamane Siriwardhana, Rivindu Weerasekera, Elliott Wen, Tharindu Kaluarachchi, Rajib Rana, and Suranga Nanayakkara. 2023. Improving the domain adaptation of retrieval augmented generation (RAG) models for open domain question answering. Transactions of the Association for Computational Linguistics 11 (2023), 1–17.
- Yutao Zhu, Huaying Yuan, Shuting Wang, Jiongnan Liu, Wenhan Liu, Chenlong Deng, Zhicheng Dou, and Ji-Rong Wen. 2023. Large language models for information retrieval: A survey. arXiv preprint arXiv:2308.07107 (2023).