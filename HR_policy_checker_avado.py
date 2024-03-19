import streamlit as st
import openai


def get_openai_client(api_key, endpoint):
    openai.api_type = 'azure'
    openai.api_key = api_key
    openai.api_version = '2023-12-01-preview'
    openai.api_base = endpoint
    return openai

def gpt_function(client, hr_policy, sector, country, query):
   
    """
    Function to call the GPT API and return a response.
    """
    user_content = f"""
    Company Policy: {hr_policy} #The policy of the company, which will be used to check alignment with legal standards and best practices try understand each and every context of policy provided to you.
    Sector: {sector}  # The sector in which the company operates.
    Country: {country}  # The country where the company is located.
    
    Use the provided company policy, sector, and country information to ensure alignment with legal standards and best practices.
    Provide a detailed response to the user's question, considering the specific policies of <Company Name>.

    
    Answer the question below as a Policy checker for <Company name> 
    Question: "{query}"  # The question asked by the user for the policy checker.
"""

    conversation = [
        {"role": "system", "content": """You are a Policy checker bot 
                        
                        Few details about the <Company name>, employees who stay within 50 miles radius of the office have to work from the office; others can leverage WFH.
                        If a woman has to work after 8 PM, she will be given cab service to her home.
                        If you are working on holidays, then 1 compensation leave and a bonus will be added to your salary at the end of the month.
                                    
                        You will be given the following information:
                            - Company policy: policy, rules, and regulations of the company
                            - Company sector: Company's working sector
                            - Country: Where the company is located
                            
                        Do the following:
                            - Report highlighting alignment with legal standards and best practices
                            - Answer the question that the user asks
                                    """},
        {"role": "user", "content": f"{user_content}"}
    ]

    response = client.ChatCompletion.create(
        messages=conversation,
        engine="gpt-35-turbo",
    )
    text_response = response.choices[0].message.content
    return text_response

def main():
    """
    Main function to create the Streamlit app.
    """
    st.title("Avado Policy Checker")

    description = """
    #### About the App
    ###### Review your HR policy against the latest industry best practices.
    """

    st.markdown(description , unsafe_allow_html=True)

    st.sidebar.title("Azure OpenAI API Key")
    openai_api_key = st.sidebar.text_input("Enter your Azure OpenAI API Key", type="password")
    openai_endpoint = 'https://bc-api-management-uksouth.azure-api.net'
    client = get_openai_client(openai_api_key, openai_endpoint)

    hr_policy = st.text_area("Company HR Policy:")
    sector = st.text_input("Company Sector:")
    country = st.text_input("Country:")
    query = st.text_input("Question:")

    if hr_policy and sector and country and openai_api_key and openai_endpoint:
        if st.button("Submit"):
            with st.spinner("Fetching the answer..."):
                output = gpt_function(client, hr_policy, sector, country, query)
                st.write(output)

if __name__ == "__main__":
    main()
