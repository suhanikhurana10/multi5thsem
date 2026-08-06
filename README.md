# Examify - AI-Powered Secure Quiz & Assessment Platform

A full-stack assessment platform that enables educators to create secure online examinations with AI-assisted grading, coding assessments, and browser-based anti-cheating mechanisms.

---

## Overview

Examify is a secure online assessment platform designed for educational institutions to conduct multiple-choice, coding, image-based, and descriptive assessments from a single interface.

The platform combines AI-powered evaluation for subjective answers, secure code execution for programming questions, and browser-based anti-cheating features to provide a scalable alternative to traditional online examination systems.

---

## Features

### Authentication & Authorization

- JWT-based authentication
- Teacher and Student role-based access
- Secure login system
- Protected REST APIs

---

### Teacher Portal

- Create and manage quizzes
- Manage question banks
- Add:
  - Multiple Choice Questions (MCQs)
  - Coding Questions
  - Descriptive Questions
  - Image-Based Questions
- Publish quizzes
- View student submissions
- View quiz analytics
- Monitor cheating violations

---

### Student Portal

- Attempt quizzes
- Integrated code editor with compilation support
- Timer-based examinations
- Real-time auto-save
- Instant results for supported question types

---

### AI-Assisted Evaluation

- Semantic grading for descriptive answers
- Sentence Transformers (**all-MiniLM-L6-v2**)
- Cosine similarity-based scoring
- Manual review support for borderline answers

---

### Coding Assessment

- Judge0 code execution integration
- Support for multiple programming languages
- Hidden test case evaluation
- Runtime and memory statistics
- Compilation error handling

---

## Anti-Cheating Features

The platform includes several browser-based mechanisms to discourage unfair practices during online examinations.

- Fullscreen enforcement
- Tab switching detection
- Window focus monitoring
- Browser visibility detection
- Copy/Paste blocking
- Clipboard restrictions
- Violation logging
- Automatic warning system
- Auto submission after a configurable violation limit
