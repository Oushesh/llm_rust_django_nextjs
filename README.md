## llm_rust_django_nextjs
    This is the frontend to test Retrieval Augmented Generation of Documents aka. Chat with Application
    In the future we will have more: DataLoaders (eg. Langchain or Langchain RS (rust) for speed) aka. Data
    Connector so all Data reside in 1 place. (confidential data from companies, slack communications, PDFs,
    gmail, etc..). This serves as a demo to test how a ChatBot behaves in the scenario where it retrieves
    data injested from different sources (PDF), encoded via Large Language Model. (eg. Ada model or DavinCi --> 1536
    dimensions.). The model is expressive enough to represent the documents in vector space.


    Upon Conversation or question, the AI agent represents the question as an embedding, gets its context. (QA Style 
    and Causal Language Modeling technique: Question as Cause and Answer as output), searches the closest representation via Distance Function (Cosine Distance, Dot Product or Eucliden Distance). Cosine Distance 
    is better since its symmetric and has -1 to +1 domain range values.

## TechStack for Frontend: 
   * Firebase Authentication 
   * NextJS 14, Edge run time 
   * React hooks, atoms for react state management, heroicons 

## Frontend 
   vercel deployment
    
   Create a project with nextjs precising typescript.
    Install the following Dependencies as well:
    * npm install recoil
    * npm install next@latest @next/font@latest
    * npm install react-hook-form
    * npm install react-hot-toast
    * npm install @heroicons/react@v1
    * npm install firebase

## Backend Deployment: 
   * https://github.com/Oushesh/llm_rust_django_backend
     deployed at: 


## Vector Database:
    supabase for vectordatabase.
    URL: https://supabase.com/dashboard/project/ercgogxayitasvdgypop/editor/28676

    The data are encoded: 

## How it looks?

![]()
![]()


