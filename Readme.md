# Loopio Translation using DeepL & Loopio API

Goal: Create a pipeline that will detect new loopio entries and translate the entries into target languages  
Value: Enable Datadog SE teams to complete RFPs faster in languages other than English 

### High-Level Process: 
1. Query the Loopio Entries to get the current state
2. Identify new or edited entries 
3. For each identified entry translate using DeepL 
4. Create a new corresponding entry in Loopio for the new language 


## Major Considerations:  
1. Tracking lineage --> How can we track the base English version for comparison / double checking? 
2. Frequency, how often does this run 
3. Resiliency --> How do we not mess up the prod Loopio entries


## Loopio API

Documentation of the different API endpoints used for Loopio
- https://developer.loopio.com/docs/loopio-api/55ef47e33f5eb-list-library-entries-you-can-interact-with
    - Argument to filter as part of the query parameters 
    - Is it possible to filter based on tags are part of the API query 
- https://developer.loopio.com/docs/loopio-api/6e8ee29b39bf0-update-core-properties-of-a-library-entry
    - Endpoint to update the properties of a library entry, will use to tag 
- https://developer.loopio.com/docs/loopio-api/bedaddd3877a9-create-a-library-entry
    - Endpoint to create a new library entry 
