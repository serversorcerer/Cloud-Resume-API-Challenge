import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ResumeData')

def lambda_handler(event, context):
    try:
        response = table.get_item(Key={'id': '1'})
        resume_data = response.get('Item', {})
        
        basics = resume_data.get('basics', {}).get('M', {})
        certificates = resume_data.get('certificates', {}).get('L', [])
        projects = resume_data.get('projects', {}).get('L', [])
        skills = resume_data.get('skills', {}).get('L', [])

        name = basics.get('name', {}).get('S', '')
        label = basics.get('label', {}).get('S', '')
        email = basics.get('email', {}).get('S', '')
        phone = basics.get('phone', {}).get('S', '')
        url = basics.get('url', {}).get('S', '')
        city = basics.get('location', {}).get('M', {}).get('city', {}).get('S', '')
        region = basics.get('location', {}).get('M', {}).get('region', {}).get('S', '')
        profiles = basics.get('profiles', {}).get('L', [])
        summary = basics.get('summary', {}).get('S', '')

        website = next((profile.get('M', {}).get('url', {}).get('S', '') for profile in profiles if profile.get('M', {}).get('network', {}).get('S', '') == 'Website'), '')
        github = next((profile.get('M', {}).get('url', {}).get('S', '') for profile in profiles if profile.get('M', {}).get('network', {}).get('S', '') == 'GitHub'), '')
        linkedin = next((profile.get('M', {}).get('url', {}).get('S', '') for profile in profiles if profile.get('M', {}).get('network', {}).get('S', '') == 'LinkedIn'), '')

        output = [
            "="*64,
            f"{name.center(64)}",
            f"{label.center(64)}",
            f"{city}, {region}".center(64),
            f"Email: {email} | Phone: {phone}".center(64),
            f"Website: {url}".center(64),
            f"GitHub: {github} | LinkedIn: {linkedin}".center(64),
            "="*64,
            "Summary:",
            summary,
            "-"*64,
            "Certificates:",
            "-"*64
        ]

        for cert in certificates:
            cert_data = cert.get('M', {})
            cert_name = cert_data.get('name', {}).get('S', '')
            cert_issuer = cert_data.get('issuer', {}).get('S', '')
            cert_date = cert_data.get('date', {}).get('S', '')
            output.append(f"- {cert_name}")
            output.append(f"  Issuer: {cert_issuer} | Date: {cert_date}")
            output.append("")

        output.append("-"*64)
        output.append("Projects:")
        output.append("-"*64)

        for i, project in enumerate(projects, 1):
            proj_data = project.get('M', {})
            proj_name = proj_data.get('name', {}).get('S', '')
            proj_start_date = proj_data.get('startDate', {}).get('S', '')
            proj_end_date = proj_data.get('endDate', {}).get('S', '')
            proj_description = proj_data.get('description', {}).get('S', '')
            proj_highlights = proj_data.get('highlights', {}).get('L', [])
            proj_url = proj_data.get('url', {}).get('S', '')

            output.append(f"{i}. {proj_name}")
            output.append(f"   Start Date: {proj_start_date} | End Date: {proj_end_date}")
            output.append(f"   - {proj_description}")
            for highlight in proj_highlights:
                output.append(f"   - {highlight.get('S', '')}")
            if proj_url:
                output.append(f"   - Project URL: {
