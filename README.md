# AI-Workflow-Agent-Platform-for-Internal-Operations

<img width="1006" height="522" alt="image" src="https://github.com/user-attachments/assets/4dfc33f8-e10c-4acc-bd34-f62bceb6691e" />

## Introduction
Every day, people at work receive emails, reports, complaints, and requests. Someone has to read each one, figure out what it is, write a response, and send it to the right person. This takes a lot of time and people often make mistakes because they are tired or busy.
This project builds a system that does all of that work automatically. When a new document or email comes in, the system reads it, understands what it is, writes a good response, and sends it to the right team. Nobody has to do anything manually. It just happens on its own, fast and correctly, every single time.
The system works with tools that companies already use like Gmail and Google Sheets so there is nothing new to learn and nothing to change about how the company already works.

## Statement of Problem
Imagine you work in an office and every morning 50 letters arrive at your desk. Each letter is different. Some are complaints. Some are requests. Some are reports. You have to read every single one, decide who should handle it, write a reply, and send it to the right person. By the time you finish, half the day is gone and you have not done any of your real work yet.
This is what happens in many companies every single day. People spend hours doing work that does not need a human brain. It is slow, tiring, and full of small mistakes.
This project fixes that problem by putting a smart AI assistant in the middle. The AI reads everything, sorts it, responds to it, and sends it where it needs to go. The people in the office can then focus on the work that actually needs them.

## Project Objectives

•	To automate repetitive reading, summarizing, and drafting tasks using cerebras.

•	To reduce manual work and save time across daily operations.

•	To improve the speed and clarity of internal communication and reporting.

•	To integrate AI into existing tools without changing how teams already work.

## Tech Stack (Simple + Professional)
•	Cerebras API: The AI brain that reads each incoming document, classifies it into the correct category, and generates a professional response tailored to the right audience. 

•	n8n (Automation / Workflow Engine): The backbone that connects everything together. It watches for new form submissions, triggers the cerebras calls, handles routing decisions, saves results, and sends emails automatically. 

•	Google Forms (Input / Trigger): The entry point where documents, requests, complaints, and inquiries are submitted. Each submission automatically feeds into Google Sheets and triggers the workflow. 

•	Google Sheets (Data Store / Log): Stores every submission alongside its cerebras classification, generated response, routing decision, and timestamp for tracking and dashboard use. 

•	Gmail (Output / Delivery): Sends the final AI generated response to the correct team based on the document classification. 

•	JavaScript (Custom Processing): Handles data cleaning, formats Gemini output before routing, and powers the monitoring dashboard. 

•	Streamlit (Monitoring Dashboard): Displays live insights from the Google Sheets data including documents processed over time, category breakdown, and daily processing volume.

## Project Workflow 

i.	A person submits a document, request, complaint, or inquiry through the Google Form

ii.	The form response lands automatically in a connected Google Sheet

iii.	n8n detects the new row in Google Sheets and triggers the workflow

iv.	n8n sends the submitted text to cerebras for classification. cerebras returns one of four categories: Report, Request, Complaint, or Inquiry

v.	n8n sends the original text and the classification back to cerebras. cerebras generates a professional response tailored to the correct audience

vi.	A JavaScript cleans and formats the cerebras output to make sure it is consistent and readable

vii.	n8n routes the formatted response to the correct team based on the classification: Reports go to management, Complaints go to customer service, Requests go to operations, and Inquiries go to the general response team

viii.	The original input, classification, cerebras response, routing decision, and timestamp are saved back into Google Sheets

ix.	Gmail sends the formatted AI response to the routed email address automatically

x.	The Streamlit dashboard reads from Google Sheets and updates live to show processing activity and category trends

 
## Project Implementation Phases
### Phase 1: AI (Cerebras) Setup

Phase 1 establishes the AI foundation of the system by generating a cerebras API key, securely connecting cerebras to n8n using the HTTP Request node, resolving server and port issues, and testing the integration to confirm stable responses. In this phase, we configured and validated a combined prompt that performs both document classification and professional response generation in strict JSON format, ensuring clean, structured output that can be parsed and routed automatically. By the end of Phase 1, the AI engine is fully connected, tested, and proven ready to power the workflow.

#### 1.1 Get Cerebras API key from Google AI Studio
•	Go to: https://www.cerebras.ai/

•	On the left sidebar, click “API Keys”

•	Click “Create API Key”

<img width="975" height="428" alt="image" src="https://github.com/user-attachments/assets/f9e8f061-2d54-473d-9a02-dad95e5ca4e6" />

•	Copy the key immediately.
•	Paste it somewhere safe (Notepad or password manager).

#### 1.2 Connect Cerebras to n8n using the HTTP Request node
•	Go to your n8n URL

•	Click New Workflow

•	Click +

•	Search: Manual Trigger, Add it

•	Click +

•	Search: HTTP Request, Add it

•	Connect it to the Manual Trigger

•	Configure HTTP Request Node

•	Method: POST

•	URL: https://api.cerebras.ai/v1/chat/completions

•	Header Name: Authorization

•	Header Value: Bearer YOUR_API_KEY

•	Authentication: None

•	Under header

•	Name: Content-Type

•	Value: application/json

•	Body Content Type: JSON

```
{
  "model": "llama3.1-8b",
  "messages": [
    {
      "role": "user",
      "content": "Say hello"
    }
  ],
  "temperature": 0.2
}
```
•	Click Execute Node

#### 1.3 Write two combined prompts: one for classification and one for response generation
•	Replace the JSON in the http node with the below
```
{
  "model": "llama3.1-8b",
  "temperature": 0,
  "messages": [
    {
      "role": "system",
      "content": "You are an AI workflow assistant for internal company operations."
    },
    {
      "role": "user",
      "content": "Step 1: Classify the document into ONLY one of these categories: Report, Request, Complaint, Inquiry.\n\nStep 2: Based on the classification, generate a professional internal response.\n\nReturn the final answer ONLY in this STRICT JSON format:\n{\n  \"category\": \"One of Report, Request, Complaint, Inquiry\",\n  \"summary\": \"Short summary of the document\",\n  \"recommended_action\": \"Clear next step\",\n  \"draft_response\": \"Professional email-style response\"\n}\n\nDo not add explanations. Do not add markdown. Return valid JSON only.\n\nDocument:\n\"A customer is unhappy about delayed delivery and poor communication.\""
    }
  ]
}

```

### Phase 2: Input Setup (Google Forms)
Phase 2 focuses on building the structured entry point of the system by creating a Google Form to collect submissions such as reports, requests, complaints, and inquiries, and linking it to a Google Sheet where all responses are stored automatically. This phase also connects n8n to the Google Sheet using a trigger node so that every new submission instantly activates the workflow. By the end of Phase 2, the system can reliably capture incoming documents and automatically pass them into the automation pipeline for AI processing.

#### 2.1	Create a Google Form with fields for name, document type description, and full text of the submission
•	Go to Google Forms → click Blank.

•	Form title: Internal Operations Submission Form

•	Description (optional): Submit reports, requests, complaints, or inquiries here. Our team will respond automatically.
 <img width="975" height="263" alt="image" src="https://github.com/user-attachments/assets/b1563026-42d1-4740-98a2-4e4ed2564aba" />


##### Create 3 questions:
•	Full Name
    Question type: Short answer
    
    Toggle: Required = ON
    
    3 dots → Response validation
    
    Text → Length → Minimum character count = 2
    
    Custom error text: Please enter your name.

 <img width="930" height="406" alt="image" src="https://github.com/user-attachments/assets/04902c36-2a69-47bb-8a45-e626da054cd3" />

•	Document Type Description
    Question type: Short answer
    
    Required = ON
    
    Help text (optional): Example: delivery issue, staff request, weekly report, inquiry about policy

 <img width="882" height="262" alt="image" src="https://github.com/user-attachments/assets/52da65aa-5566-4719-908c-77472f8d4f5d" />


•	Full Submission Text
    Question type: Paragraph
    
    Required = ON
    
    Help text (optional): Paste the full message here. Include any important details.
    
 <img width="917" height="183" alt="image" src="https://github.com/user-attachments/assets/374c5835-1a04-421e-9299-90d321f375f3" />


##### Click the gear icon (Settings):

•	Collect email addresses: OFF (unless you want it)

•	Limit to 1 response: OFF

•	Allow response editing: OFF

•	Make this a quiz: OFF

<img width="974" height="374" alt="image" src="https://github.com/user-attachments/assets/52de29b0-a3d1-4512-a17f-2bbde3d39a9d" />

 
Click on publish

<img width="975" height="337" alt="image" src="https://github.com/user-attachments/assets/69c6c2df-6f12-4b78-82b8-29d47c4f100c" />

 


#### 2.2	Connect the form to a Google Sheet so responses populate automatically

•	Go to your Google Form.

•	Click on the “Responses” tab at the top.
 
 <img width="878" height="357" alt="image" src="https://github.com/user-attachments/assets/2e98dae9-8201-4306-b21a-aea00f8a8a8d" />


•	Click the small green Google Sheets icon (it says “Create spreadsheet” when you hover on it).

•	Choose “Create a new spreadsheet.”

•	Click Create.

<img width="1009" height="338" alt="image" src="https://github.com/user-attachments/assets/c9d8851e-3a99-4610-abd1-f79338c40289" />


#### 2.3	Connect n8n to the Google Sheet using the Google Sheets trigger node
In n8n, create the trigger workflow

•	New Workflow

•	Add node: Google Sheets Trigger
•	In the node, set: Event: New Row (or “On New Row Added” depending on your n8n version)
 
<img width="1009" height="338" alt="image" src="https://github.com/user-attachments/assets/8b5686c7-56d8-4f32-95a4-f54812ea5fae" />


Connect Google credentials

•	In the node, under Credentials, click Create New

•	Choose Google Sheets OAuth2 (recommended)

•	Click Sign in with Google

•	Allow permissions
 
<img width="975" height="433" alt="image" src="https://github.com/user-attachments/assets/3ad2b22a-06ce-4c83-b37b-8d4ab18af14d" />

Under Document

•	From list, select the goggle sheet just created

•	Under sheets, select form responses 1

 <img width="1005" height="321" alt="image" src="https://github.com/user-attachments/assets/45037dcc-339d-471c-92ae-5f4d26649a96" />


Test the trigger

•	Click Listen for test event (or “Test step”)

<img width="966" height="305" alt="image" src="https://github.com/user-attachments/assets/345bad21-9f44-4323-9908-e122a9171e3c" />

 
•	Go to your Google Form and submit one test response

•	Come back to n8n; it should capture the new row
 <img width="1013" height="238" alt="image" src="https://github.com/user-attachments/assets/2c732860-9351-46c4-81bb-33960cf84dcd" />


Now that our Google Sheets is connected, we need to prevent duplicate processing because the trigger can re-run the same row again. We will add a simple deduplication check before the AI runs.

We will:

•	Add a column in the form response sheet named Processed

 <img width="975" height="142" alt="image" src="https://github.com/user-attachments/assets/28f0579f-1f81-4c3b-a454-32abd9cf7520" />


Add IF Node (Right After Google Sheets Trigger)

Value 1 (Expression): {{$json.Processed}}

Type: String

Operation: is empty

##### Meaning

•	TRUE → Processed is empty → NEW → Continue workflow

•	FALSE → Processed has something (YES) → STOP

 <img width="900" height="241" alt="image" src="https://github.com/user-attachments/assets/d4cf868c-6edd-4b48-9348-c489dc976220" />


### Phase 3: Processing (Two-Step Cerebras Reasoning)
Phase 3 is the intelligence core of the entire system. In this stage, the workflow moves beyond simply collecting submissions and begins actively understanding and responding to them. Using a structured two-step reasoning approach, the first cerebras call classifies each incoming document into one of four defined categories, ensuring clear routing logic. The second cerebras call then uses both the original text and the classification result to generate a professional, context-aware response tailored to the appropriate internal audience. By separating classification and response generation, this phase ensures accuracy, clarity, and structured output that is fully ready for automated routing, storage, and email delivery in the next stages of the workflow.

#### 3.1	Send the form submission text to Cerebras with the prompt "Classify this document as one of the following: Report, Request, Complaint, or Inquiry. Return only the category name"
•	In your workflow (in the true branch), click +

•	Add HTTP Request node. Connect: True branch → HTTP Request

Configure the HTTP Request node

•	Method: POST

•	URL: https://api.cerebras.ai/v1/chat/completions

•	Header Name: Authorization

•	Header Value: Bearer YOUR_API_KEY

•	Authentication: None

•	Headers: Content-Type = application/json

 <img width="742" height="666" alt="image" src="https://github.com/user-attachments/assets/9778d90a-6eb4-44c5-b96d-ed786050d7ff" />

•	Body Content Type: JSON

•	Body (Classifier Prompt): Paste this JSON (and only replace the “Document” part with your n8n field mapping):
```
{
  "model": "llama3.1-8b",
  "temperature": 0,
  "messages": [
    {
      "role": "system",
      "content": "You classify documents into ONLY ONE of these categories: Report, Request, Complaint, Inquiry. You must return ONLY valid JSON in this exact format: {\"category\":\"Report\"}. Do not add explanations. Do not add markdown. Do not add extra text."
    },
    {
      "role": "user",
      "content": "Classify this document:\n\n{{ $json['Full Submission Text'] }}"
    }
  ]
}

```
 
<img width="975" height="498" alt="image" src="https://github.com/user-attachments/assets/f80e44a0-9e45-4f9b-bdc8-7ec46d3e5bac" />


#### 3.2	Send the classification result and original text back to cerebras with the prompt "Based on the classification above, generate a clear and professional response for a [role] audience"
Add the second HTTP Request node

•	In your workflow, click +
•	Add a new node: HTTP Request

•	Connect it like this:

AI_Request_Classifer → AI_Response_Generator 

<img width="636" height="282" alt="image" src="https://github.com/user-attachments/assets/f93f894b-655e-4fe3-b436-d70f63af2c28" />


Configure the HTTP Request node

•	Method: POST

•	URL: https://api.cerebras.ai/v1/chat/completions

•	Header Name: Authorization

•	Header Value: Bearer YOUR_API_KEY

•	Authentication: None

•	Headers: Content-Type = application/json

•	Body Content Type: JSON

•	Body (Classifier Prompt): Paste this JSON 
```
{{
JSON.stringify({
  "model": "llama3.1-8b",
  "temperature": 0,
  "messages": [
    {
      "role": "system",
      "content": "You are an internal operations assistant. You must return ONLY valid JSON with this exact structure: {\"category\":\"Report|Request|Complaint|Inquiry\",\"draft_response\":\"...\"}. Do not add explanations. Do not add markdown. Do not add extra text."
    },
    {
      "role": "user",
      "content": "Classification: " 
        + ($node["AI_Request_Classifier"].json.choices?.[0]?.message?.content || "")
        + "\n\nWrite a clear and professional response for the appropriate internal team.\n\nReturn ONLY valid JSON exactly like this:\n{\n  \"category\": \"Report|Request|Complaint|Inquiry\",\n  \"draft_response\": \"A professional email-style response\"\n}\n\nDocument:\n"
        + ($json["Full Submission Text"] || "")
    }
  ]
})
}}

```
<img width="975" height="674" alt="image" src="https://github.com/user-attachments/assets/427e4e45-58e1-4494-8223-b361c20f9134" />





### Phase 4: JavaScript Data Cleaning
Phase 4 focuses on refining and standardizing the AI-generated output before it moves into routing and delivery. While cerebras produces structured JSON responses, minor inconsistencies such as spacing, formatting variations, or capitalization differences can occur. In this phase, a lightweight JavaScript script is introduced to clean, validate, and properly structure the output into a consistent, professional email-ready format. This ensures reliability across different inputs and guarantees that every response entering the routing and email stages is polished, readable, and operationally safe for automated deployment.

#### 4.1	Write a JS script that receives the raw Cerebras output

•	Click +. Add node: Code (select JavaScript)

Connect it like this: AI_Response_Generator → JavaScript_Cleaner
 
<img width="836" height="287" alt="image" src="https://github.com/user-attachments/assets/294906f0-326e-4a37-8946-992ddb2302ec" />

•	Paste this JS inside the node
```
// Runs once for all items and returns one output per input item
return items.map((item) => {
  const classifierRaw =
    item?.$node?.AI_Request_Classifier?.json?.choices?.[0]?.message?.content
    || $node["AI_Request_Classifier"].json?.choices?.[0]?.message?.content
    || "";

  let category = "";
  try {
    const cleaned = String(classifierRaw).replace(/```json|```/gi, "").trim();
    const parsed = JSON.parse(cleaned);
    category = parsed?.category ? String(parsed.category) : String(classifierRaw);
  } catch (e) {
    category = String(classifierRaw);
  }

  category = category.replace(/[\r\n\t]/g, "").trim();
  category = category.toLowerCase();
  category = category.charAt(0).toUpperCase() + category.slice(1);

  const generatorRaw =
    item?.$node?.AI_Response_Generator?.json?.choices?.[0]?.message?.content
    || $node["AI_Response_Generator"].json?.choices?.[0]?.message?.content
    || "";

  const cleanedGen = String(generatorRaw).replace(/```json|```/gi, "").trim();
  const match = cleanedGen.match(/\{[\s\S]*\}/);

  let draft_response = "";
  let error = null;

  if (match) {
    try {
      const parsedGen = JSON.parse(match[0]);
      draft_response = parsedGen?.draft_response ? String(parsedGen.draft_response).trim() : cleanedGen;
      if (!parsedGen?.draft_response) error = "Generator JSON missing draft_response; raw output used";
    } catch (e) {
      draft_response = cleanedGen;
      error = "Generator JSON parsing failed; raw output used: " + e.message;
    }
  } else {
    draft_response = cleanedGen;
    error = "No JSON object found in generator output; raw output used";
  }

  return {
    json: {
      ...(item.json || {}),
      category,
      draft_response,
      original_query: item.json?.["Full Submission Text"],
      ...(error ? { error } : {})
    }
  };
});

```
<img width="975" height="270" alt="image" src="https://github.com/user-attachments/assets/c756f533-d741-4089-8488-28632407769e" />




### Phase 5: Intelligent Routing
Phase 5 focuses on intelligent routing, where the cleaned and structured AI output is automatically directed to the correct internal team based on its classification. Using an n8n Switch node, the system evaluates whether a submission is a Report, Complaint, Request, or Inquiry, and then routes it to the appropriate email destination such as management, customer service, operations, or the general response team. This phase ensures that every document not only receives an AI-generated response but is also delivered to the right department without manual intervention, maintaining accuracy, speed, and operational efficiency.

#### 5.1	Add an n8n Switch node after the JavaScript cleaning step

•	Open your workflow

•	Click the + after your JavaScript_Cleaner node

•	Add node: Switch

•	Connect it like this: JavaScript_Cleaner → Switch

<img width="990" height="378" alt="image" src="https://github.com/user-attachments/assets/8e09a07e-5089-4bfa-99ff-a9d6373f6302" />

 

#### 5.2	Configure four routes based on cerebras classification
Set the “Value to Check”

•	In the Switch node, look for “Value 1” (or “Expression” depending on your version)

•	Set it to this expression:

={{$json.category}}

Add 4 rules (one per category)

Set Mode to something like “Rules” or “Equal” checks.

Create these rules:
1.	Rule 1

o	Operation: Equals

o	Value: Report

2.	Rule 2

o	Operation: Equals

o	Value: Complaint

3.	Rule 3

o	Operation: Equals

o	Value: Request

4.	Rule 4

o	Operation: Equals

o	Value: Inquiry
 
<img width="976" height="897" alt="image" src="https://github.com/user-attachments/assets/ccf63e91-4edd-4b1e-b3a3-456a6c620cdd" />

•	Click Add options, Fallback Output and select Extra Output

<img width="770" height="245" alt="image" src="https://github.com/user-attachments/assets/557d46e6-cfa7-48a4-a986-2fce241b7220" />

 
•	Now let us configure 

o	Report goes to management team email

o	Complaint goes to customer service email

o	Request goes to operations team email

o	Inquiry goes to general response email

#### Create 4 “Set” nodes to attach destination emails (recommended)
This is the cleanest routing style: Switch decides the path, then each path sets the destination email.
For each Switch output, add a Set node:

Path 1 (Report → Management)

Add Set node named: Set_Management

Set fields:

•	Drag from the Report output dot of the Switch.

•	Click + Add node → Set

•	Rename it: Set_Management

Inside Set_Management:

•	Click Add Field

•	Field name: to_email

•	Type: String

•	Value: management@yourcompany.com

Add another field:

•	Field name: team

•	Value: Management

Toggle on include other input field
<img width="907" height="514" alt="image" src="https://github.com/user-attachments/assets/84aad7a4-d7c7-4a4d-b7f0-801e8ffe89d9" />

 
Repeat the above process for others

Path 2 (Complaint → Customer Service)

Set_CustomerService

•	to_email = customerservice@yourcompany.com

•	team = Customer Service

Path 3 (Request → Operations)

Set_Operations

•	to_email = operations@yourcompany.com

•	team = Operations

Path 4 (Inquiry → General Response)

Set_General

•	to_email = info@yourcompany.com

•	team = General Response

Click add option, Fallback output then output complaint

<img width="914" height="492" alt="image" src="https://github.com/user-attachments/assets/3374b552-4a9b-4008-92b0-fdb81f76b5af" />

 

#### Phase 6: Save Result
Phase 6 ensures that every processed submission is permanently recorded for accountability, reporting, and monitoring purposes. In this stage, the workflow writes the cleaned AI output back into Google Sheets, storing the original submission, its classification, the generated response, the routing destination, and a timestamp. This creates a reliable audit trail of all processed documents, enables performance tracking, and provides the live data source required for the monitoring dashboard in Phase 8. By the end of this phase, no submission is lost, and the entire system becomes measurable, transparent, and fully traceable.

#### 6.1	Add a Google Sheets write step in n8n after routing

•	Click the + after Set_Management

•	Search and Google Sheets

•	Operation: Append Row

•	Connect it like this: Set_Management → Google_Sheets_Save
 
<img width="606" height="277" alt="image" src="https://github.com/user-attachments/assets/02a0b8e0-ec4a-486a-b3e1-420f1f07b22c" />


Configure the Google Sheets Node

•	Credentials: Use the same Google Sheets OAuth2 credential you used earlier.

•	Resource: Spreadsheet

•	Operation: Append

•	Document: Select your Form response spreadsheet

•	Sheet: create a new sheet called: Processed_Logs

(Recommended: create a clean sheet just for processed results.)

 <img width="661" height="608" alt="image" src="https://github.com/user-attachments/assets/8530ce77-af77-41db-8742-042b0b37257f" />


#### 6.2	Save the following for every submission: original input, classification, cerebras response, routing destination, and timestamp

•	Open your Google Sheet → tab Processed_Logs → Row 1 headers (exactly like this):

o	Original_Input

o	Category

o	Cerebras_Response

o	Routing_Destination

o	Timestamp
 
<img width="975" height="79" alt="image" src="https://github.com/user-attachments/assets/8cb17af9-b21e-49b5-a657-03fada32211e" />

•	Open your Google Sheets Save node. Under mapping column mode, select map each column manually:

o	Original_Input ={{$node["Google Sheets Trigger"].json["Full Submission Text"]}}

o	Category ={{$json.category}}

o	Cerebras_Response ={{$json.draft_response}}

o	Routing_Destination {{ $json['to_email '] }}

o	Timestamp ={{$now}}


•	Click add options, Cell format and select let n8n format
 <img width="664" height="366" alt="image" src="https://github.com/user-attachments/assets/91858894-62f3-49d9-a9bc-cabc88b06a30" />


Now duplicate the node to all set nodes, your work flow should look like the below

 <img width="975" height="486" alt="image" src="https://github.com/user-attachments/assets/5b31be1d-5b71-4549-b68b-43674840dcbc" />



#### 6.3	Confirm all records are saving correctly with no missing fields

We filled the google form, came to the n8n and clicked execute and the response was saved in our Processed_Logs
 <img width="1104" height="91" alt="image" src="https://github.com/user-attachments/assets/f492545e-6f40-4d24-936c-b5c89e724aa6" />


### Phase 7: Send Result (Gmail)
Phase 7 is where the system sends the message. After the AI reads the document, understands it, writes a reply, and chooses the right team, the system now sends the email by itself. No person needs to press send. The correct team receives the message immediately. This is the final step that makes the whole process complete and automatic.

•	Click the + after Google_Sheets_Save (on the Management route first)

•	Add Gmail

•	Choose Operation: Send Email
 
<img width="717" height="298" alt="image" src="https://github.com/user-attachments/assets/34876a07-3302-415a-81bb-c558e90e3ba7" />

•	Connect your Gmail OAuth2 credentials

Configure the Gmail node (works for all routes)
•	To:
```
{{ $json.Routing_Destination }}
```

•	Subject:
```
{{"[" + $json.Category + "] " + "Auto Response" + " | " + $json.Timestamp}}
```
•	Email Body:
```
Hello Team,

A new submission has been processed and routed.

Document Category: {{$json.Category}}
Timestamp: {{$json.Timestamp}}

AI Draft Response:
{{$json.Cerebras_Response}}

Original Submission:
{{$json.Original_Input}}

Regards,
AI Workflow Assistant
```
<img width="975" height="688" alt="image" src="https://github.com/user-attachments/assets/abe8fd32-97ad-4188-b230-75c6ba310dd5" />


Duplicate to other nodes, your workflow should be like the below
<img width="975" height="316" alt="image" src="https://github.com/user-attachments/assets/8e63075e-11df-432a-963b-1e04e67506ef" />

 
### Phase 8: Processing State Management & Re-Run Control

Phase 8 ensures that every submission has a clearly defined processing state, preventing duplicate execution while allowing controlled reprocessing when necessary. This phase introduces structured status management within Google Sheets so the workflow can intelligently determine whether a row should be processed, skipped, retried, or flagged for review. By implementing this control layer, the system becomes production-ready, resilient to trigger replays, and operationally transparent.

•	Click + after Gmail, Add Google Sheets

•	Operation: Update

•	Sheet: Form Responses 1 (NOT Processed_Logs)

•	Under column to match on, click processed

•	Under processed, type YES


Very important, under column to match on, select timestamp, drag and drop it from input
 
<img width="805" height="775" alt="image" src="https://github.com/user-attachments/assets/534cf929-4867-4103-930a-1db87ddc45ee" />


<img width="1760" height="628" alt="image" src="https://github.com/user-attachments/assets/55e7a57a-4993-4c29-972b-38836fcdca3c" />

#### Phase 9: Monitoring Dashboard (Streamlit)
Phase 9 transforms the automation system into a fully observable and data-driven operational platform by introducing a live monitoring dashboard built with Streamlit. In this phase, the dashboard connects directly to the Google Sheets Processed_Logs sheet using the gspread Python library, allowing it to read newly processed records in real time. It then visualizes key performance insights including total documents processed over time (line chart), distribution by category (pie chart), and daily processing volume (bar chart). By the end of this phase, management gains instant visibility into workflow activity, AI performance trends, and operational workload, making the system not just automated, but measurable, transparent, and strategically valuable.

#### Create the Service Account email

•	Google Cloud Console → Service Accounts

Go to: Google Cloud Console → search “Service Accounts” in the top search bar → open it.

•	Make sure you’ve selected the correct Project (top left dropdown). If you don’t have any, create one quickly.

•	Click + CREATE SERVICE ACCOUNT

•	Fill:

•	Service account name: streamlit-dashboard

•	Click CREATE AND CONTINUE

•	On the “Grant this service account access” page:

•	Click CONTINUE (no role needed)

•	Click DONE

After this, you will see a new row with an email that looks like:

streamlit-dashboard@xxxxx.iam.gserviceaccount.com

Share your Google Sheet with that email (give it access)

•	Open your Google Sheet (the one with Processed_Logs).

•	Click Share (top-right).

•	In the “Add people and groups” box, paste this email:

streamlit-dashboard@streamlit-dashboard-489113.iam.gserviceaccount.com

•	Set permission to Viewer (or Editor if you want it to write—Viewer is enough for dashboard).

•	Click Send.

#### Note: Make sure you enable google sheet and google drive api

 <img width="1038" height="441" alt="image" src="https://github.com/user-attachments/assets/01c26603-24b3-4940-9631-1ceaebd86c09" />


Go back to
```
https://console.cloud.google.com/
```

•	Go to:

IAM & Admin → Service Accounts

•	Click the service account:

streamlit-dashboard@streamlit-dashboard-489113.iam.gserviceaccount.com

•	Go to the Keys tab.

•	Click:

➕ Add Key → Create new key

•	Choose:

JSON

•	Click Create

It would download a file like this

streamlit-dashboard-489113-xxxx.json

SSH into your vps

•	Run the below commands
```
mkdir -p ~/dashboards/internal_ops_dashboard
cd ~/dashboards/internal_ops_dashboard
 ```
<img width="975" height="230" alt="image" src="https://github.com/user-attachments/assets/ec2c64a4-da96-4582-b200-bfda0c26e55f" />

•	Upload the JSON File to VPS. From your local computer terminal (NOT inside VPS), run
```
scp /path/to/your/downloaded-file.json root@YOUR_SERVER_IP:/root/dashboards/internal_ops_dashboard/service_account.json
``` 
<img width="975" height="253" alt="image" src="https://github.com/user-attachments/assets/12374e60-a346-4031-871b-65fdf813f95a" />

•	Run this command;
```
chmod 600 service_account.json
ls -l
``` 
<img width="975" height="265" alt="image" src="https://github.com/user-attachments/assets/a6406fbf-417b-4791-afae-158778ca6687" />

•	Run the following codes to install dependencies;
```
python3 -m venv venv
source venv/bin/activate
pip install plotly
pip install streamlit gspread google-auth pandas matplotlib
```
<img width="975" height="364" alt="image" src="https://github.com/user-attachments/assets/96122a8e-d4f3-4d9a-8360-dfb03db7ee0e" />
 

Create the Streamlit Dashboard (Full Working Version)

•	Create an app.py file and paste the below;

[app.py](https://github.com/Ogbunugafor-Philip/AI-Workflow-Agent-Platform-for-Internal-Operations/blob/main/internal_ops_dashboard/app.py)


•	Run the below to see the dashboard
```
streamlit run app.py --server.port 8507 --server.address 0.0.0.0
```

<img width="975" height="469" alt="image" src="https://github.com/user-attachments/assets/73b27252-3562-4b61-98e3-513d6bbc5607" />
 

Our dashboard only runs when we run the above command. Now, lets make it run always
•	Run the below commands
```
sudo tee /etc/systemd/system/internal-ops-dashboard.service > /dev/null <<'EOF'
[Unit]
Description=Internal Ops Streamlit Dashboard
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/dashboards/internal_ops_dashboard

Environment=PYTHONUNBUFFERED=1
Environment=STREAMLIT_SERVER_PORT=8507
Environment=STREAMLIT_SERVER_ADDRESS=0.0.0.0

ExecStart=/root/dashboards/internal_ops_dashboard/venv/bin/python -m streamlit run app.py --server.port 8507 --server.address 0.0.0.0

Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF
```

•	Run this also;
```
sudo systemctl daemon-reload
sudo systemctl restart internal-ops-dashboard
sudo systemctl enable internal-ops-dashboard
```

•	Update firewall to accept the port. Run;
```
sudo ufw allow 8507/tcp
sudo ufw status
``` 

<img width="975" height="289" alt="image" src="https://github.com/user-attachments/assets/07b05599-9899-4c1a-831f-61fa1ad39c87" />

•	To access our dashboard, paste the below on your browser
```
http://<ip_address>:8507
``` 

<img width="975" height="467" alt="image" src="https://github.com/user-attachments/assets/b1f24c1b-e151-432d-9a82-04594d128199" />


### Conclusion
This AI Workflow and Agent Platform for Internal Operations deliver a complete end to end automation system that captures internal submissions, understands them with Cerebras, generates professional responses, routes them to the correct teams, and logs everything for accountability. By combining Google Forms, Google Sheets, n8n, and Gmail, the workflow fits naturally into tools teams already use, removing repetitive manual work while improving the speed, clarity, and consistency of internal communication across reports, requests, complaints, and inquiries.
With the Streamlit monitoring dashboard running continuously through systemd, the solution also becomes fully observable and production ready. Management can track real time activity, category trends, and daily processing volume, while the processing state management prevents duplicate handling and supports controlled reprocessing when needed. Overall, the platform turns internal operations into a faster, smarter, and measurable process that allows teams to focus on more important work instead of routine message handling.

