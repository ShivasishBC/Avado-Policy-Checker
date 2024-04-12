import streamlit as st
import openai

def get_openai_client(api_key, endpoint):
    openai.api_type = 'azure'
    openai.api_key = api_key
    openai.api_version = '2023-12-01-preview'
    openai.api_base = endpoint
    return openai
    
def gpt_function(client,policy_type, hr_policy, sector, country):
    """
    Function to call the GPT API and return a response.
    """
    user_content = f"""
    Policy Type : {policy_type}
    Company Policy: {hr_policy}
    Sector: {sector}
    Country: {country}
    
    Use the provided Policy Type , company policy, sector, and country information to ensure alignment with legal standards and best practices.
    Provide a report highlighting alignment with industry best practices, including a summary of country best practices, alignment of your policy with regional best practices, and recommendations for greater alignment in british english.
"""

    conversation = [
        {"role": "system", "content": """You are a Policy Proofer bot 
                        
                        You will be given the following information in details with proper format and subheadings including Company Sector (Sector) , Country Located (Country):
                        
                         - Use this below Headings ad markdown
                                1. #### Summary of {policy_type}
                                2. #### Best practices in {country}
                                2. #### How Your Policy compares 
                                3. #### Recomandations to improve your policy
                                    """},
        {"role": "user", "content": f"{user_content}"}
    ]

    response = client.ChatCompletion.create(
        messages=conversation,
        engine="gpt-35-turbo",
        temperature = 0

    )
    text_response = response.choices[0].message.content
    return text_response


def main():
    """
    Main function to create the Streamlit app.
    """
    st.title("Policy Proofer")

    description = """
    ###### Review your HR policy against best practice in your region
    """
    st.markdown(description , unsafe_allow_html=True)


    st.sidebar.title("Azure OpenAI API Key")
    openai_api_key = st.sidebar.text_input("Enter your Azure OpenAI API Key", type="password")
    openai_endpoint = 'https://bc-api-management-uksouth.azure-api.net'
    client = get_openai_client(openai_api_key, openai_endpoint)

    
    policy_type = st.text_input("Policy Type:")
    hr_policy = st.text_area("Copy and paste the HR policy that you want to check")
    sector = st.text_input("Company Sector:")
    country = st.selectbox(
    'Select your Country:',
    ('India', 'UK', 'Australia', 'USA', 'Canada', 'Germany', 'France'))
    if hr_policy and sector and country and openai_api_key and openai_endpoint:
        if st.button("Submit"):
            with st.spinner("Saving you time..."):
                output = gpt_function(client, policy_type, hr_policy, sector, country)
                st.write(output)

if __name__ == "__main__":
    main()
