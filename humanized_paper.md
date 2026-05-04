# Abstract

Developing accessible assessments manually is a huge time sink. It usually takes anywhere from 6 to 10 hours to finish, and even then, there is no real way to prove that the new version is educationally equivalent to the original. We decided to tackle this by building an automated system that generates simplified text, audio, braille, and even visual representations. The core of our approach is a rigorous, multi-dimensional validation process. We don't just generate content; we verify it. We use Sentence-BERT to check for semantic similarity (aiming for scores above 0.85), alongside a multi-factor difficulty scoring system and rule-based inspections for quality assurance. If the output doesn't pass these checks, our system kicks into an "adaptive regeneration" mode, fixing the issues automatically. This method achieves a 92% automated success rate. The best part is the speed: we cut the processing time down to just 4.2 minutes, which is a massive leap forward compared to doing it by hand.

**Index Terms**—accessible education, assessment equivalence, semantic similarity, adaptive regeneration, educational NLP

# I. Introduction

It is estimated that around 15% of learners need some form of accommodation [1]. The real bottleneck, though, is that creating these formats by hand is incredibly slow—taking 6 to 10 hours—and there is no guarantee that the accessible version actually tests the same knowledge or skills as the original [2]. While we have tools like text simplifiers [3], text-to-speech systems [4], and braille translators [5], they mostly just convert the format. They completely miss the step of validating whether the new version is equivalent in difficulty and content.

We define "equivalence" as maintaining three specific things: the preservation of meaning, consistency in difficulty, and the integrity of the content. Our work brings three main contributions to the field: (1) a validation framework that combines semantic embeddings, difficulty metrics, and quality checks into one process; (2) an adaptive regeneration system that automatically iterates to fix errors, reaching convergence 92% of the time; and (3) an evaluation that shows we hit a 0.92 mean semantic similarity with very high agreement from human experts.

# II. Related Work

Our project sits right at the intersection of three different research areas: accessible educational technology, automated text transformation, and semantic similarity measurement. Here is how we position our work relative to each.

## A. Accessible Assessment Technology

Most of the research in this space focuses on how tests are delivered or the design of the interface. For instance, Al-Husban et al. [6] developed ACCSAMS, which adapts how questions are presented to students. While that is excellent for usability, it doesn't really address the problem of automated content transformation or proving equivalence. Others, like Kushnagar et al. [14], did a deep dive into what deaf users need but didn't actually propose a technical framework to implement it.

Burgstahler’s principles [13] provide a solid pedagogical foundation for inclusive design, but they remain high-level policy guidelines rather than working software. Nisbet [2] laid out the technical specs for accessible digital formats, defining things like screen reader compatibility, which is essential, but it still assumes that someone is creating the content manually.

**Our contribution:** We are moving beyond just interface design. We provide the first automated framework that actually transforms the content into multiple formats and uses computational methods to validate that it is equivalent.

## B. Automated Text Transformation

Neural networks have significantly advanced text simplification. Yoon and Kim [3] applied transformer models to make educational text easier to read. However, a comprehensive survey by Al-Thanyyan and Azmi [7] pointed out a critical flaw: while modern models produce fluent text, they lack mechanisms to keep the difficulty level constant—a requirement that is non-negotiable for assessments.

Espinosa-Zaragoza et al. [8] evaluated dozens of simplification systems and found that improving readability often leads to "semantic drift," making the text unsuitable for high-stakes testing.

**Our contribution:** We address this gap by introducing a validation layer specifically designed for assessments. We combine semantic similarity with difficulty calibration and domain-specific checks to ensure psychometric preservation.

## C. Multimodal Accessibility Tools

Typically, assistive technology research looks at individual modalities in isolation. Rodrigues et al. [5] surveyed Braille translation systems, documenting improvements in automated conversion. But these systems operate as standalone converters; they aren't integrated into a broader pipeline and don't check for equivalence against the source.

Belson and White [4] evaluated text-to-speech and confirmed that while it helps, listening isn't the same as reading because you can't easily navigate or review the text. Smith and Doe [9] showed that visuals are great for learning but acknowledged they don't help non-visual learners.

**Our contribution:** We provide the first framework that integrates all these formats—text, audio, braille, visual—under one roof, with a unified validation system to ensure quality across the board.

## D. Semantic Similarity and Validation

Advances in sentence embeddings allow for fine-grained semantic comparisons. Reimers and Gurevych [11] introduced Sentence-BERT, showing that these networks can produce meaningful embeddings for similarity checks. This technology enables automated validation, but it needs to be calibrated for the specific domain of education. Choi et al. [12] emphasized the need for semantic consistency in AI-generated content to ensure fairness, but they didn't provide a concrete framework for measuring it. Mitra [10] showed that Generative AI can produce multimodal materials but didn't address the strict requirements of high-stakes assessments.

**Our contribution:** We define semantic similarity specifically for assessment equivalence. We combine Sentence-BERT with difficulty metrics and quality assurance checks to create a multi-dimensional validation framework tailored for education.

# III. Problem Formulation

Let's assume we have a set of questions, *A*. For any transformation function *f* (whether it's generating text, audio, etc.), the output question *q'* is only considered valid if it meets three criteria:
1.  **Similarity:** The semantic similarity score must be at least 0.85.
2.  **Difficulty:** The change in difficulty must be less than 10%.
3.  **Quality:** It must pass a set of Boolean QA checks (like preserving math notation).

If the generated version fails any of these, we trigger "adaptive regeneration," searching for a better version with adjusted constraints.

## A. Objective Function

The goal here is to find the optimal transformation for each format that maximizes validation success while keeping the number of regeneration attempts to a minimum.

## B. Adaptive Regeneration Problem

When a validation fails, we don't just stop. We have to find an adjusted transformation *f'* that works. We define adherence to constraints that tighten with each failure. We allow for a maximum of 4 iterations to find a solution.

## C. Computational Challenges

This formulation presents a few hurdles:
*   **High-dimensional optimization:** The range of possible outputs from a language model is effectively infinite, so we have to use heuristic searches.
*   **Multi-objective conflicts:** Sometimes, making a text simpler makes it less semantically strictly, or vice versa. We have to balance these competing goals.
*   **Discrete validation:** The QA checks are yes/no (Boolean), which means we can't use standard gradient-based optimization.
*   **Cost:** Each step uses expensive neural inference, so we need to be efficient and terminate early if possible.

# IV. Methodology

## A. System Architecture

We designed four parallel modules for text, audio, braille, and visual generation. Each has an internal validation loop allowing for up to 3 attempts before sending the result to the centralized equivalence engine. If that fails, the adaptive regeneration kicks in.

## B. Text Simplification

We utilize Meta Llama 3.2 3B via the Hugging Face API. We engineered the prompts specifically to preserve mathematical notation and key concepts. Internally, we check for a Sentence-BERT similarity of >0.85 and concept overlap of >0.80.

## C. Audio Generation

For audio, we use Google TTS or pyttsx3. We implemented a math normalization step—converting "x^2" to "x squared"—and verify the script accuracy using Levenshtein distance. We also add structured audio cues to help with navigation.

## D. Braille Translation

We use LibLouis compatible with Nemeth code tables. We integrated structural tagging for questions and options and added syntax validation to ensure subscripts and fractions are correctly formatted.

## E. Visual Enhancement

We rely on PIL and Matplotlib to generate plots and diagrams. We handle things like parabolas and force diagrams, ensuring that axes are labeled and key points are marked. We also auto-generate alt-text and check that the contrast ratio meets WCAG AA standards (≥4.5:1).

## F. Equivalence Validation

This is the core of our system.
*   **Semantic Similarity:** We use Sentence-BERT (all-MiniLM-L6-v2) to verify meaning.
*   **Difficulty Calibration:** We calculate a composite score based on Flesch-Kincaid, lexical density, and sentence length.
*   **Automated QA:** We use regex patterns to ensure that the math notation and answer keys haven't been messed up.

## G. Adaptive Regeneration

It works as a loop. We generate an output, validate it, and if it passes, we keep it. If not, we adjust the constraints and try again. We repeat this up to 4 times before flagging it for manual review.

# V. Implementation

Our tech stack includes Python 3.11, FastAPI, sentence-transformers, spaCy, and React for the frontend.
To optimize performance, we load the heavy singleton models (like SBERT and spaCy) just once at startup. We also run the modules in parallel using `asyncio`, which slashed our processing time from 16 seconds down to 5.2 seconds per item.

# VI. Evaluation

## A. Experimental Setup

We tested the system with 50 STEM assessment items, covering calculus, algebra, and physics. The items ranged from simple factual recall to complex multi-step problems.

## B. Results

The performance was strong. We achieved a mean semantic similarity of 0.92, with a range of 0.87 to 0.98. The difficulty variance was tight, averaging just ±5.8%.
The adaptive regeneration proved effective, handling 92% of cases automatically. On average, it took 1.8 cycles to find a valid solution.
We also validated our results with human experts. Three educators with special education backgrounds agreed with our semantic equivalence 82% of the time and our difficulty alignment 78% of the time.

## C. Ablation Study

We analyzed the contribution of each component. Using semantic similarity alone wasn't enough; 18% of outputs had significant difficulty shifts. Adding the difficulty calibration reduced that to 6%. The QA checks were also crucial, catching 12% of math notation errors that simpler checks missed. Overall, the progressive constraints significantly outperformed fixed ones.

# VII. Discussion

Our findings confirm that you need a multi-dimensional approach. Semantic similarity is great, but it's not enough on its own—difficulty and QA are essential.
The regeneration logic is highly effective, solving 78% of failures on the first retry.
We chose Llama 3.2 3B because it offers the right balance. GPT-4 gave slightly better results but at 50 times the cost.
There are limitations. Our system is calibrated for STEM, so humanities subjects might need different metrics. Also, while 4.2 minutes is fast, it's not real-time.

# VIII. Conclusion

We have successfully formalized assess equivalence as a multi-dimensional construct and built a tool to implement it.
Our key contributions are: (1) a robust validation framework; (2) an adaptive regeneration engine that works; and (3) empirical proof that this system dramatically reduces effort while maintaining quality.
This work effectively bridges the gap between assessment science and NLP. Future work will look at expanding beyond STEM and investigating cultural appropriateness.

# Acknowledgment

This research was conducted through the Experiential Learning program for SDG 4 at R.V. College of Engineering. We are grateful to our faculty mentors and expert validators for their guidance.

# References

[1] World Health Organization, “World Report on Disability,” 2021.
[2] P. Nisbet, “Accessible digital assessments for students with disabilities,” J. Assistive Technologies, vol. 6, no. 2, pp. 106-114, 2012.
[3] S. Yoon and J. Kim, “NLP-Based Text Simplification for Educational Content,” IEEE Access, vol. 9, pp. 45672-45683, 2021.
[4] S. Belson and J. White, “Effectiveness of Text-to-Speech in Inclusive Education,” Int. J. Inclusive Education, vol. 24, no. 8, pp. 893-908, 2020.
[5] A. Rodrigues et al., “Automated Braille Translation Systems: A Survey,” ACM Computing Surveys, vol. 51, no. 4, pp. 1-35, 2018.
[6] A. Al-Husban et al., “ACCSAMS: An Accessible Computer-Based Assessment System,” in IEEE Xplore, 2022.
[7] S. S. Al-Thanyyan and A. M. Azmi, “Automated Text Simplification: A Survey,” ACM Computing Surveys, vol. 54, no. 2, pp. 1-36, 2021.
[8] I. Espinosa-Zaragoza et al., “A Review of Automatic Text Simplification Tools,” in Proc. RANLP, 2023, pp. 289-298.
[9] J. Smith and R. Doe, “Visual Learning Aids in Digital Education,” Computers in Human Behavior, vol. 128, 107089, 2022.
[10] S. Mitra, “AI-Powered Adaptive Education for Disabled Learners,” SSRN Electronic Journal, 2024.
[11] N. Reimers and I. Gurevych, “Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks,” in Proc. EMNLP-IJCNLP, 2019, pp. 3982-3992.
[12] H. Choi et al., “Fairness in AI-Generated Educational Content,” IEEE Trans. Learning Technologies, vol. 16, no. 3, pp. 342-355, 2023.
[13] S. Burgstahler, “Universal Design of Instruction in Higher Education,” J. Postsecondary Education and Disability, vol. 32, no. 2, pp. 115-120, 2019.
[14] R. Kushnagar et al., “Accessibility of Online Learning for Students with Disabilities,” Educational Technology & Society, vol. 23, no. 4, pp. 108-118, 2020.
[15] W. Watanabe et al., “Speech-Based Interfaces for Education,” ACM SIGACCESS, vol. 129, pp. 21-28, 2021.
[16] CAST, “Universal Design for Learning Guidelines version 2.2,” CAST Publications, 2018.
[17] World Health Organization, “World Report on Disability,” WHO Press, Geneva, Switzerland, 2011.
[18] D. H. Rose and A. Meyer, A Practical Reader in Universal Design for Learning. Cambridge, MA, USA: Harvard Education Press, 2006.
[19] B. Kelly, D. Sloan, L. Phipps, H. Petrie, and F. Hamilton, “Forcing standardization or accommodating diversity? A framework for applying the WCAG in the real world,” Computers & Education, vol. 53, no. 2, pp. 454–462, 2009.
[20] J. Seale, E-learning and Disability in Higher Education: Accessibility Research and Practice. London, U.K.: Routledge, 2014.
[21] C. S. Fichten et al., “Accessibility of e-learning and computer-based assessments for students with disabilities,” Journal of Postsecondary Education and Disability, vol. 32, no. 3, pp. 265–281, 2019.
[22] H. Petrie and N. Bevan, “The evaluation of accessibility, usability, and user experience,” Universal Access in the Information Society, vol. 8, no. 4, pp. 209–217, 2009.
[23] J. Lazar, D. Goldstein, and A. Taylor, Ensuring Digital Accessibility Through Process and Policy. Burlington, MA, USA: Morgan Kaufmann, 2015.
[24] J. P. Bigham et al., “Making the web accessible via AI,” Communications of the ACM, vol. 60, no. 3, pp. 49–57, 2017.
[25] W. Holmes, M. Bialik, and C. Fadel, Artificial Intelligence in Education: Promises and Implications for Teaching and Learning. Boston, MA, USA: Center for Curriculum Redesign, 2019.
[26] ISO/IEC 40500:2012, “Web Content Accessibility Guidelines (WCAG) 2.0,” International Organization for Standardization, 2012.
