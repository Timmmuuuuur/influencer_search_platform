import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict
from openai import OpenAI

# Initialize OpenAI client only if API key is available
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key and api_key != "your_openai_api_key_here" else None

async def send_outreach_email(match, campaign) -> bool:
    """
    Send personalized outreach email to influencer
    """
    try:
        # Generate personalized email content
        email_content = await generate_outreach_email(match, campaign)
        
        # Email configuration
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        email_username = os.getenv("EMAIL_USERNAME")
        email_password = os.getenv("EMAIL_PASSWORD")
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = email_username
        msg['To'] = match.influencer.email or "contact@example.com"  # Fallback email
        msg['Subject'] = email_content['subject']
        
        # Add body
        msg.attach(MIMEText(email_content['body'], 'html'))
        
        # Send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_username, email_password)
        text = msg.as_string()
        server.sendmail(email_username, msg['To'], text)
        server.quit()
        
        print(f"Email sent successfully to {match.influencer.name}")
        return True
        
    except Exception as e:
        print(f"Email sending error: {e}")
        return False

async def generate_outreach_email(match, campaign) -> Dict:
    """
    Generate personalized outreach email using AI
    """
    try:
        # Get product and company details
        product = match.product
        company = campaign.company
        influencer = match.influencer
        
        prompt = f"""
        Write a professional, personalized outreach email for influencer collaboration. The email should be:
        - Professional but friendly
        - Personalized to the influencer's content
        - Clear about the collaboration opportunity
        - Include specific details about the product
        - Mention the fit score and why they're a good match
        - Include a clear call-to-action
        
        Return a JSON response with:
        {{
            "subject": "Email subject line",
            "body": "HTML email body"
        }}
        
        Details:
        - Company: {company.name}
        - Product: {product.name} - {product.description}
        - Influencer: {influencer.name} ({influencer.channel_title})
        - Influencer Categories: {influencer.content_categories}
        - Fit Score: {match.fit_score:.2f}
        - Estimated Price: ${match.price_estimate}
        - Influencer Subscribers: {influencer.subscriber_count:,}
        - Average Views: {influencer.avg_views:,}
        - Engagement Rate: {influencer.engagement_rate:.2%}
        """
        
        if not client:
            return {
                "subject": f"Collaboration Opportunity - {product.name}",
                "body": generate_fallback_email(match, campaign)
            }
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert in influencer marketing and email outreach. Write compelling, personalized emails that build genuine relationships with influencers. Always return valid JSON format."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        import json
        result = json.loads(response.choices[0].message.content)
        
        # Ensure HTML formatting
        if 'body' in result:
            result['body'] = format_email_html(result['body'])
        
        return result
        
    except Exception as e:
        print(f"Email generation error: {e}")
        return {
            "subject": f"Collaboration Opportunity - {product.name}",
            "body": generate_fallback_email(match, campaign)
        }

def format_email_html(body: str) -> str:
    """
    Format email body as HTML
    """
    # Basic HTML formatting
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .header {{ background-color: #f4f4f4; padding: 20px; text-align: center; }}
            .content {{ padding: 20px; }}
            .footer {{ background-color: #f4f4f4; padding: 20px; text-align: center; font-size: 12px; }}
            .cta-button {{ background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="content">
            {body.replace('\n', '<br>')}
        </div>
    </body>
    </html>
    """
    return html_body

def generate_fallback_email(match, campaign) -> str:
    """
    Generate a fallback email if AI generation fails
    """
    product = match.product
    company = campaign.company
    influencer = match.influencer
    
    return f"""
    <div class="header">
        <h2>Collaboration Opportunity with {company.name}</h2>
    </div>
    
    <div class="content">
        <p>Dear {influencer.name},</p>
        
        <p>I hope this email finds you well! I'm reaching out from {company.name}, and I've been following your amazing content on YouTube. Your videos on {', '.join(influencer.content_categories or ['your niche'])} are truly engaging!</p>
        
        <p>We have an exciting collaboration opportunity that I believe would be a perfect fit for your channel and audience. We're looking to partner with creators who share our values and can authentically represent our product.</p>
        
        <h3>About Our Product</h3>
        <p><strong>{product.name}</strong><br>
        {product.description}</p>
        
        <h3>Why You're a Great Match</h3>
        <ul>
            <li>Your content aligns perfectly with our brand (Fit Score: {match.fit_score:.1%})</li>
            <li>Your {influencer.subscriber_count:,} subscribers match our target audience</li>
            <li>Your {influencer.engagement_rate:.1%} engagement rate shows an active, engaged community</li>
        </ul>
        
        <h3>Collaboration Details</h3>
        <ul>
            <li>Product: {product.name}</li>
            <li>Compensation: ${match.price_estimate}</li>
            <li>Content: 1 video featuring our product</li>
            <li>Timeline: Flexible based on your schedule</li>
        </ul>
        
        <p>We'd love to discuss this opportunity further and answer any questions you might have. Would you be interested in a brief call to learn more?</p>
        
        <a href="mailto:{campaign.company.email}" class="cta-button">Reply to Discuss</a>
        
        <p>Thank you for considering this partnership. We're excited about the possibility of working together!</p>
        
        <p>Best regards,<br>
        The {company.name} Team</p>
    </div>
    
    <div class="footer">
        <p>This email was sent because we believe you're a great fit for our brand. If you're not interested, no worries - just let us know!</p>
    </div>
    """