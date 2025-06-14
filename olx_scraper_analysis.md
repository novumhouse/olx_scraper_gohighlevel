# OLX Job Scraper Analysis

## Data Structure Observed

From analyzing the OLX job listings, I've identified the following data structure:

1. **Job Listings Page**:
   - Contains multiple job listings with basic information
   - Each listing has a title, company name (sometimes), and a link to detailed page
   - Listings are paginated with "ponad 1000 ogłoszeń" (over 1000 listings)

2. **Job Detail Page**:
   - Contains complete information about the job
   - Company name is clearly displayed
   - Position title is in the heading
   - Contact information (phone number) is hidden behind a "Zadzwoń / SMS" button
   - Clicking the button reveals the phone number

## Data to Extract

For each job listing that matches our criteria (manufacturing companies, not agencies):

1. **Company Name**: 
   - Example 1: "Mubea" 
   - Example 2: "POLAK MEBLE"

2. **Position**: 
   - Example 1: "Operator Maszyn (produkcja automotive)"
   - Example 2: "Krojcza - Operator Lagowarki i Cuttera"

3. **Phone Number**: 
   - Example 1: "77 549 30 84"
   - Example 2: "511-341-826"

## Filtering Criteria

To identify manufacturing companies and exclude employment agencies:

1. Look for keywords in company descriptions that indicate manufacturing:
   - "producent" (manufacturer)
   - "produkcja" (production)
   - "fabryka" (factory)
   - "zakład" (plant)
   - Industry-specific terms like "meble" (furniture), "automotive", etc.

2. Exclude listings with agency indicators:
   - "agencja pracy" (employment agency)
   - "agencja zatrudnienia" (recruitment agency)
   - "agencja pośrednictwa pracy" (job placement agency)
   - Company names of known agencies

## Technical Implementation Plan

The application will need to:

1. Navigate to the OLX job listings page for production jobs
2. Iterate through job listings pages
3. For each listing:
   - Check if it appears to be from a manufacturing company (not an agency)
   - Open the detailed job page
   - Extract company name and position
   - Click the "Zadzwoń / SMS" button to reveal the phone number
   - Extract the phone number
   - Store the data
4. Send the collected data to GoHighLevel API

## GoHighLevel Integration

The data will be sent to GoHighLevel as contacts with:
- Company name
- Position (can be stored in a custom field)
- Phone number
- Source (OLX)
- Date collected

