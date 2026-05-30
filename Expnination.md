# Energybae AI Internship Project Explanation

This file is a beginner-friendly explanation of the full project so you can confidently explain it in an interview, demo, or viva.

---

## 1. Project Title

**Electricity Bill to Excel Automation for Solar Load Calculation**

---

## 2. Simple One-Line Explanation

This project takes an electricity bill as input, extracts important values automatically using AI, fills those values into an Excel template, preserves all formulas, calculates the solar load, and gives the user a ready-to-use output file.

---

## 3. Business Problem

Energybae works in solar and renewable energy. Their team receives electricity bills from customers and manually enters bill data into an Excel file to calculate:

- average electricity usage
- solar panel requirement
- solar capacity
- number of solar panels
- total solar capacity

This manual process is slow, repetitive, and error-prone.

So the goal of the project is to automate this work.

---

## 4. Main Objective

The goal is to build a system where:

1. User uploads a bill image or PDF
2. The system reads the bill automatically
3. The system extracts required data
4. The extracted data is inserted into the provided Excel template
5. Existing Excel formulas remain untouched
6. Solar calculations are produced automatically
7. User downloads the completed file

---

## 5. Actual Workflow of This Project

Here is the real end-to-end flow of the system we built:

1. The user opens the web app
2. The user uploads one or more bill images or PDFs
3. The backend validates file types
4. If the upload is a PDF, pages are converted into images
5. Images are preprocessed to improve extraction quality
6. The bill is sent to an AI model for extraction
7. The AI returns structured JSON
8. The backend validates and normalizes the extracted data
9. The extracted data is shown in the UI for review
10. The user can correct any field manually
11. The system fills only the Excel input cells
12. Formula cells remain unchanged
13. Cached values are also written so calculated cells are visible immediately
14. The user downloads the final Excel file
15. If more than two bills are uploaded, the system creates multiple Excel files and returns them as a ZIP

---

## 6. Tech Stack Used

### Backend

- **FastAPI**
- **Python**

Why:
- Fast to build
- Clean API structure
- Good for file upload and backend logic
- Easy to explain in interview

### Frontend

- **HTML**
- **CSS**
- **Vanilla JavaScript**
- **Jinja2 templates**

Why:
- No React or heavy frontend setup needed
- Faster for internship submission
- Enough for upload, preview, review, and download flow

### AI Extraction

- **Gemini API** or **OpenAI API**

Why:
- Needed for low-quality image understanding
- Can extract structured data from complex electricity bills
- Better than plain OCR for noisy, multilingual bills

### Excel Automation

- **openpyxl**

Why:
- Lets us open and edit `.xlsx` files
- Allows writing only input cells
- Keeps formulas safe

### PDF/Image Handling

- **PyMuPDF**
- **OpenCV**

Why:
- PDF pages must be converted into images
- Image preprocessing improves extraction quality

---

## 7. Why This Stack Is a Good Choice

This stack is good because:

- it is fast to develop
- it is practical for an internship
- it is easy to demo
- it supports AI extraction
- it supports Excel writing
- it is production-friendly enough for a business automation MVP

If the interviewer asks why you did not use React or a complex architecture, you can say:

> I optimized for working delivery, speed, clarity, and maintainability. Since the main challenge was AI extraction and Excel automation, I used a lightweight frontend and focused on reliable backend logic.

---

## 8. File and Folder Structure

```text
AI_agent/
  app/
    api/
    models/
    services/
    static/
    templates/
  assets/
    samples/
    template.xlsx
  docs/
  generated/
  tests/
  README.md
  Expnination.md
  requirements.txt
```

### What each folder does

- `app/api/` contains routes like extract and generate
- `app/models/` contains request and response schemas
- `app/services/` contains business logic
- `app/static/` contains JavaScript and CSS
- `app/templates/` contains the HTML page
- `assets/` stores the Excel template and sample bills
- `generated/` stores final outputs
- `tests/` stores unit tests

---

## 9. Important Project Files

### [app/main.py](/c:/Users/hp/OneDrive/Pictures/Desktop/AI_agent/app/main.py)

Starts the FastAPI app.

### [app/api/routes.py](/c:/Users/hp/OneDrive/Pictures/Desktop/AI_agent/app/api/routes.py)

Contains API endpoints:

- home page
- extract bill data
- generate Excel output
- provider status

### [app/services/extraction_service.py](/c:/Users/hp/OneDrive/Pictures/Desktop/AI_agent/app/services/extraction_service.py)

Handles AI extraction using Gemini or OpenAI.

### [app/services/excel_service.py](/c:/Users/hp/OneDrive/Pictures/Desktop/AI_agent/app/services/excel_service.py)

Handles Excel writing, preserves formulas, and writes visible calculated values.

### [app/services/validation_service.py](/c:/Users/hp/OneDrive/Pictures/Desktop/AI_agent/app/services/validation_service.py)

Validates and normalizes extracted data.

### [app/services/sample_data_service.py](/c:/Users/hp/OneDrive/Pictures/Desktop/AI_agent/app/services/sample_data_service.py)

Supports local extraction fallback for the exact sample images provided in the task.

### [docs/analysis.md](/c:/Users/hp/OneDrive/Pictures/Desktop/AI_agent/docs/analysis.md)

Contains analysis of the task brief, bill samples, Excel structure, formulas, and mapping.

---

## 10. Problem Analysis Before Coding

One important strength of this project is that we did not jump directly to coding. We first analyzed:

- the internship brief
- the sample bill images
- the Excel template
- input cells
- formula cells
- output dependencies

This is important in an interview because it shows engineering thinking.

You can say:

> I first reverse-engineered the Excel template and identified which cells are editable and which are calculated. That helped me build a safe automation flow without breaking the business formulas.

---

## 11. Excel Template Understanding

The template is used to calculate solar load and panel recommendations.

It contains:

- customer details
- fixed charges
- sanctioned load
- connection type
- 12 months of electricity units
- bill amount
- formula-based solar calculations

### Key calculated fields

- Average
- kW
- Solar Panels
- Solar capacity
- Number of Panels
- Total solar capacity
- Number of solar panels

### Very important point

We never overwrite formula cells. We only fill input cells.

This is one of the most important things to say in the interview.

---

## 12. Mapping Logic

The application maps bill data into the Excel sheet.

Example:

- Consumer Name → `D1` or `H1`
- Consumer Number → `D2` or `H2`
- Fixed Charges → `D3` or `H3`
- Sanctioned Load → `D4` or `H4`
- Connection Type → `D5` or `H5`
- Monthly units → `D9:D20` or `H9:H20`
- Bill Amount → `E20` or `I20`

The full mapping is documented in [docs/analysis.md](/c:/Users/hp/OneDrive/Pictures/Desktop/AI_agent/docs/analysis.md).

---

## 13. How AI Extraction Works

The system reads the uploaded bill and sends the image to an AI model.

The model is prompted to return structured JSON containing:

- utility name
- consumer name
- consumer number
- address
- mobile number
- meter number
- bill month
- bill year
- bill date
- due date
- payable amount
- fixed charges
- Excel bill amount
- sanctioned load
- connection type
- tariff category
- previous reading
- current reading
- units consumed
- 12-month usage history

### Why AI instead of OCR only

Electricity bills are messy:

- low-quality mobile photos
- mixed Marathi and English
- non-tabular layout
- history shown in chart/list form

OCR alone often gives broken text. AI vision is better at understanding layout and context.

---

## 14. Data Validation Logic

After extraction, the app does not trust the raw AI result blindly.

It validates things like:

- current reading minus previous reading should roughly match units consumed
- missing fixed charges should be flagged
- missing bill amount should be flagged
- monthly history should be normalized to a 12-month window

This is important because AI extraction is probabilistic, not perfect.

You can say:

> I added validation after extraction because AI can read data incorrectly, so I wanted the system to catch mismatches before exporting to Excel.

---

## 15. Why the Review Screen Exists

The review screen is there because in business automation, full automation is ideal, but reviewability is very important.

It allows the user to:

- see extracted values
- correct wrong values
- verify ambiguous fields
- confirm before final export

This improves reliability and user trust.

---

## 16. How Excel Generation Works

This is the most important technical part.

The app:

1. Opens the provided Excel template
2. Finds the sheet
3. Writes only the mapped input fields
4. Leaves formulas unchanged
5. Calculates visible result cache values for formula cells
6. Saves the final file
7. Returns the file for download

### Why we added cached values

Some Excel viewers show formula cells as blank until Excel recalculates them. To solve that, the project also writes cached values so the output appears filled immediately.

This was an important bug fix in the project.

---

## 17. Multi-Bill Support

Originally the template had space for only two bills.

To support up to five uploaded bills, the system now works like this:

- bills are processed in groups of two
- each group fills one Excel workbook
- if more than two bills are uploaded, multiple workbooks are generated
- those workbooks are returned inside a ZIP file

This is a practical business solution because the original template itself is limited to two bill sections.

---

## 18. Error Handling

The project handles:

- invalid file types
- missing API key
- missing extracted fields
- incomplete monthly history
- poor image quality
- multi-bill batch output
- Excel generation issues

This is good to mention because interviewers often ask about edge cases.

---

## 19. Real Challenges Faced

You should be honest about the challenges. Good interview answers are realistic.

### Challenge 1: Excel field ambiguity

The `Bill Amount` in the Excel sample did not exactly match the large payable amount visible on the bill image.

### What we did

We documented the ambiguity, allowed user review, and used a practical fallback strategy.

### Challenge 2: Formula cells looked blank in exported file

The formulas were preserved, but cached display values were empty.

### What we did

We preserved formulas and also wrote cached calculated values to the workbook.

### Challenge 3: Template supports 2 bills, but business may upload more

### What we did

We added grouped workbook generation and ZIP output for up to 5 bills.

### Challenge 4: Low-quality bill photos

### What we did

We added image preprocessing and AI-based extraction.

---

## 20. Architecture Explanation

Here is the architecture in simple words:

### Frontend

- upload bill
- preview bill
- show extracted data
- allow edit
- generate Excel
- download result

### Backend

- receive file
- validate file
- convert PDF if needed
- preprocess image
- call AI model
- validate data
- fill Excel
- return output

### Output Layer

- single `.xlsx` for 1-2 bills
- `.zip` of `.xlsx` files for 3-5 bills

---

## 21. Architecture Diagram You Can Explain

```text
User
  |
  v
Web UI
  |
  v
FastAPI Backend
  |
  +--> File Validation
  |
  +--> PDF/Image Preprocessing
  |
  +--> AI Extraction
  |
  +--> Validation + Normalization
  |
  +--> Excel Template Fill
  |
  v
Download Output (.xlsx / .zip)
```

---

## 22. Why This Is a Good Internship Project

This project shows multiple skills together:

- problem analysis
- Python backend development
- AI integration
- document understanding
- Excel automation
- validation design
- frontend basics
- production thinking

This makes it a strong internship submission because it is not just a toy UI. It solves a real business workflow.

---

## 23. What to Say in Demo

Here is a simple demo explanation:

> This tool automates Energybae’s electricity bill analysis workflow. A user uploads one or more electricity bills, the system extracts the relevant fields using AI, normalizes the values, fills the provided Excel template without changing formulas, calculates solar sizing fields like average usage and panel count, and returns a ready-to-use output file. If more than two bills are uploaded, the system creates multiple filled workbooks and returns them as a ZIP.

---

## 24. Short 1-Minute Interview Answer

If the interviewer says “Explain your project in one minute”, say:

> I built an AI-powered bill-to-Excel automation system for Energybae. The problem was that their team manually reads electricity bills and fills an Excel sheet to calculate solar sizing. I first analyzed the provided bill samples and the Excel template to understand the required fields, input cells, and formula cells. Then I built a FastAPI-based web app where users upload bill images or PDFs, the system extracts data using an AI vision model, validates and normalizes the values, and fills the original Excel template without overwriting formulas. I also handled multi-bill uploads, export generation, and formula display issues by writing cached calculated values into the workbook so the output is immediately usable.

---

## 25. Medium 2-Minute Interview Answer

If the interviewer gives you more time, say:

> This project automates a manual business workflow used in solar sales. The user uploads an electricity bill, the system reads it using an AI model, extracts fields like consumer number, sanctioned load, units consumed, and billing values, and maps them into a provided Excel template that already contains business formulas for solar sizing. My first step was to analyze the actual workbook structure and reverse-engineer which cells were inputs versus formulas. I used FastAPI for the backend, a lightweight HTML and JavaScript frontend for the UI, OpenCV and PyMuPDF for bill preprocessing, and openpyxl for Excel writing. A key engineering decision was to preserve all original Excel formulas and only write into safe input cells. I also added validation, user review, support for up to five uploaded bills, and batch ZIP output because the original workbook supports only two bill sections. The final output is a ready-to-use Excel file that matches the manual process much more closely while saving time.

---

## 26. If They Ask “What Did You Build Yourself?”

You can say:

> I built the overall solution design, the FastAPI backend, the upload and extraction API flow, the field mapping logic, the validation rules, the Excel writer, the multi-bill batching logic, the review UI, and the documentation around the workbook structure and formula safety.

---

## 27. If They Ask “Why Did You Use FastAPI?”

Answer:

> I used FastAPI because it is lightweight, fast to develop, and very suitable for file upload APIs and structured JSON responses. It also keeps the architecture clean and interview-friendly.

---

## 28. If They Ask “Why Not Only OCR?”

Answer:

> The sample bills are low-quality and mixed-language, and some important fields are not in a simple table. OCR alone can extract text, but it often struggles to understand layout and context. AI vision helps extract structured information more reliably from messy bill images.

---

## 29. If They Ask “How Did You Protect Excel Formulas?”

Answer:

> I first analyzed the workbook to identify editable cells and formula cells. In the export layer I only write to mapped input cells. I never overwrite formula cells. I also keep the formulas in place and write cached output values so the results appear immediately in the generated file.

---

## 30. If They Ask “How Did You Handle Multiple Bills?”

Answer:

> The provided template supports two bill sections. To handle up to five uploaded bills, I grouped bills in pairs, generated one workbook per pair, and returned a ZIP file when more than two bills were uploaded.

---

## 31. If They Ask “What Were the Main Risks?”

Answer:

> The main risks were incorrect extraction from poor-quality images, ambiguity in some bill amount fields, and damaging the Excel workbook formulas. I reduced those risks using preprocessing, validation, editable review, and strict formula-safe export logic.

---

## 32. If They Ask “What Would You Improve Next?”

Good answer:

> If I had more time, I would add stronger OCR fallback, support for more electricity board formats, persistent storage for uploads and outputs, user authentication, audit logs, and a feedback loop to improve extraction prompts over time.

---

## 33. If They Ask “Is It Production Ready?”

Balanced answer:

> It is production-oriented but still internship-level. The architecture is clean and extensible, and the core workflow works end to end. For full production, I would add monitoring, authentication, storage management, retry logic, stronger fallback extraction, and support for more template variations.

---

## 34. If They Ask “How Did You Test It?”

Answer:

> I tested the normalization logic, sample-bill fallback logic, Excel date handling, and workbook output behavior. I also verified that the generated workbook preserves formulas and contains visible calculated values in important result cells.

---

## 35. Questions the Interviewer May Ask

Here are likely questions:

1. Why did you choose this architecture?
2. How does the AI extraction work?
3. How do you ensure formulas are not broken?
4. What happens if the bill is low quality?
5. How do you handle multiple uploads?
6. How do you validate extracted data?
7. Why use AI instead of OCR?
8. What are the limitations?
9. What would you improve next?
10. How would you deploy this?

---

## 36. Deployment Answer

If they ask how you would deploy it, say:

> I would containerize the app, deploy the FastAPI backend on a cloud platform like Azure App Service or Render, store uploaded files in object storage, keep generated outputs in temporary storage, and manage API keys with environment variables or a secret manager.

---

## 37. Beginner-Friendly Technical Summary

If you feel nervous, remember this simple explanation:

- The frontend collects the bill
- The backend processes the bill
- AI reads the bill
- Python validates the values
- openpyxl fills the Excel template
- formulas stay safe
- the final file is returned to the user

That is the full project in simple words.

---

## 38. Exact Features You Can Claim

You can safely say this project supports:

- upload of bill image or PDF
- preview of uploaded file
- AI-based data extraction
- extracted data review and edit
- Excel template autofill
- formula preservation
- visible calculated output values
- support for up to 5 uploaded bills
- ZIP output for multi-workbook cases

---

## 39. Honest Limitations You Should Admit

Be honest in interview. That makes you sound stronger, not weaker.

- Unknown bill formats may still need better prompt tuning
- Some bill fields can be ambiguous in poor-quality photos
- Full no-key extraction is only available for the provided sample images
- Broader production rollout would need more template and utility coverage

---

## 40. Best Final Closing Line in Interview

Use this at the end:

> This project is a practical AI automation solution for a real business workflow. My main focus was to build an end-to-end system that is accurate, safe for the Excel template, easy to explain, and useful in a real internship setting.

---

## 41. Final Advice for Your Interview

- Do not try to memorize every line
- Understand the flow
- Explain the problem first, then the solution
- Emphasize formula safety
- Emphasize AI extraction plus review
- Be honest about limitations
- Speak clearly and slowly

If you explain the project in this order, you will sound much more confident:

1. business problem
2. objective
3. architecture
4. extraction flow
5. Excel automation
6. challenges
7. improvements

---

## 42. Very Short Final Revision

If you need the shortest version:

> I built a FastAPI-based AI automation tool that reads electricity bills, extracts key values using AI, validates them, fills an existing Excel template without overwriting formulas, calculates solar sizing fields, and returns the finished Excel output. I also supported multi-bill uploads and batch output generation.

