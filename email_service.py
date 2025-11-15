import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from jinja2 import Template
import logging

class EmailService:
    def __init__(self, app=None):
        self.app = app
        self.smtp_server = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('MAIL_PORT', '587'))
        self.use_tls = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
        self.username = os.getenv('MAIL_USERNAME')
        self.password = os.getenv('MAIL_PASSWORD')
        self.default_sender = os.getenv('MAIL_DEFAULT_SENDER')
        
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def send_email(self, to_email, subject, html_content, text_content=None):
        """Send an email with both HTML and text content"""
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.default_sender
            msg['To'] = to_email
            
            # Add text version if provided
            if text_content:
                text_part = MIMEText(text_content, 'plain')
                msg.attach(text_part)
            
            # Add HTML version
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            
            self.logger.info(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False
    
    def send_premium_suggestion_email(self, user_email, user_name, suggestions):
        """Send premium service suggestion email to user"""
        subject = "Personalized Government Service Recommendations"
        
        html_template = Template("""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Service Recommendations</title>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; }
                .header { background: #0b3b8c; color: white; padding: 20px; text-align: center; }
                .content { padding: 30px 20px; }
                .suggestion { background: #f8f9fa; border-left: 4px solid #0b3b8c; padding: 15px; margin: 15px 0; }
                .suggestion-title { font-weight: bold; color: #0b3b8c; margin-bottom: 8px; }
                .suggestion-reason { font-size: 14px; color: #666; }
                .cta { background: #0b3b8c; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0; }
                .footer { background: #f8f9fa; padding: 20px; text-align: center; font-size: 12px; color: #666; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Citizen Services Portal</h1>
                <p>Personalized Service Recommendations</p>
            </div>
            
            <div class="content">
                <h2>Hello {{ user_name }},</h2>
                
                <p>Based on your recent activity on the Citizen Services Portal, we've identified some government services that might be particularly relevant to your needs.</p>
                
                <h3>Recommended Services:</h3>
                
                {% for suggestion in suggestions %}
                <div class="suggestion">
                    <div class="suggestion-title">{{ suggestion.service_name }}</div>
                    <div class="suggestion-reason">
                        Recommended because: {{ suggestion.reasons|join(', ') }}<br>
                        <strong>Relevance Score:</strong> {{ suggestion.score }}/5
                    </div>
                </div>
                {% endfor %}
                
                <h3>Premium Support Available</h3>
                <p>If you need personalized assistance with these services, our premium support team can help you:</p>
                <ul>
                    <li>Navigate complex application processes</li>
                    <li>Ensure all required documents are prepared</li>
                    <li>Get priority processing for your applications</li>
                    <li>Receive one-on-one guidance from service experts</li>
                </ul>
                
                <a href="http://127.0.0.1:5000/dashboard" class="cta">View Your Dashboard</a>
                
                <p><strong>Questions?</strong> Reply to this email or visit your dashboard for more information.</p>
                
                <p>Best regards,<br>
                The Citizen Services Team</p>
            </div>
            
            <div class="footer">
                <p>This email was sent because you have an active account on the Citizen Services Portal.</p>
                <p>You can manage your email preferences in your <a href="http://127.0.0.1:5000/profile">account settings</a>.</p>
            </div>
        </body>
        </html>
        """)
        
        text_template = Template("""
        Citizen Services Portal - Service Recommendations
        
        Hello {{ user_name }},
        
        Based on your recent activity, we've identified some government services that might be relevant to your needs:
        
        {% for suggestion in suggestions %}
        - {{ suggestion.service_name }}
          Recommended because: {{ suggestion.reasons|join(', ') }}
          Relevance Score: {{ suggestion.score }}/5
        
        {% endfor %}
        
        Premium Support Available:
        - Navigate complex application processes
        - Ensure all required documents are prepared
        - Get priority processing for your applications
        - Receive one-on-one guidance from service experts
        
        Visit your dashboard: http://127.0.0.1:5000/dashboard
        
        Best regards,
        The Citizen Services Team
        """)
        
        html_content = html_template.render(user_name=user_name, suggestions=suggestions)
        text_content = text_template.render(user_name=user_name, suggestions=suggestions)
        
        return self.send_email(user_email, subject, html_content, text_content)
    
    def send_admin_report_email(self, admin_email, report_data):
        """Send weekly admin report with user engagement insights"""
        subject = f"Weekly Admin Report - {datetime.now().strftime('%B %d, %Y')}"
        
        html_template = Template("""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Admin Report</title>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; }
                .header { background: #0b3b8c; color: white; padding: 20px; text-align: center; }
                .content { padding: 30px 20px; }
                .metric { background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; }
                .metric-value { font-size: 24px; font-weight: bold; color: #0b3b8c; }
                .metric-label { font-size: 14px; color: #666; }
                table { width: 100%; border-collapse: collapse; margin: 15px 0; }
                th, td { padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }
                th { background: #f8f9fa; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Weekly Admin Report</h1>
                <p>{{ report_date }}</p>
            </div>
            
            <div class="content">
                <h2>Engagement Summary</h2>
                
                <div class="metric">
                    <div class="metric-value">{{ report_data.total_users }}</div>
                    <div class="metric-label">Total Registered Users</div>
                </div>
                
                <div class="metric">
                    <div class="metric-value">{{ report_data.weekly_engagements }}</div>
                    <div class="metric-label">Engagements This Week</div>
                </div>
                
                <div class="metric">
                    <div class="metric-value">{{ report_data.premium_candidates }}</div>
                    <div class="metric-label">Premium Service Candidates</div>
                </div>
                
                <h3>Most Popular Services</h3>
                <table>
                    <tr><th>Service</th><th>Engagements</th></tr>
                    {% for service in report_data.popular_services %}
                    <tr><td>{{ service.name }}</td><td>{{ service.count }}</td></tr>
                    {% endfor %}
                </table>
                
                <h3>Premium Suggestions Sent</h3>
                <p>{{ report_data.emails_sent }} premium suggestion emails were sent this week.</p>
                
                <p><a href="http://127.0.0.1:5000/admin">View Admin Dashboard</a></p>
            </div>
        </body>
        </html>
        """)
        
        html_content = html_template.render(
            report_date=datetime.now().strftime('%B %d, %Y'),
            report_data=report_data
        )
        
        return self.send_email(admin_email, subject, html_content)

class PremiumSuggestionService:
    def __init__(self, db, email_service):
        self.db = db
        self.email_service = email_service
        self.users_col = db["users"]
        self.engagements_col = db["engagements"]
        self.notifications_col = db["notifications"]
    
    def analyze_premium_candidates(self):
        """Analyze user engagement patterns to identify premium service candidates"""
        # Find users with repeated engagements on similar topics
        pipeline = [
            {
                "$match": {
                    "user_id": {"$ne": None},
                    "timestamp": {"$gte": datetime.utcnow() - timedelta(days=7)}
                }
            },
            {
                "$group": {
                    "_id": {
                        "user_id": "$user_id",
                        "service": "$service"
                    },
                    "count": {"$sum": 1},
                    "questions": {"$addToSet": "$question_clicked"}
                }
            },
            {
                "$match": {"count": {"$gte": 2}}
            }
        ]
        
        candidates = list(self.engagements_col.aggregate(pipeline))
        
        # Process candidates and generate suggestions
        premium_suggestions = []
        for candidate in candidates:
            user_id = candidate["_id"]["user_id"]
            service_name = candidate["_id"]["service"]
            engagement_count = candidate["count"]
            questions = candidate["questions"]
            
            # Get user details - fix ObjectId conversion
            from bson import ObjectId
            try:
                # Try to convert string user_id to ObjectId for lookup
                if isinstance(user_id, str):
                    user_obj_id = ObjectId(user_id)
                else:
                    user_obj_id = user_id
                    
                user = self.users_col.find_one({"_id": user_obj_id})
            except:
                # If conversion fails, try direct lookup
                user = self.users_col.find_one({"_id": user_id})
                
            if not user:
                continue
            
            # Check if user has notification preferences enabled
            if not user.get("notification_preferences", {}).get("premium_suggestions", True):
                continue
            
            # Check if we've already sent a notification recently
            recent_notification = self.notifications_col.find_one({
                "user_id": user_id,
                "type": "premium_suggestion",
                "sent_at": {"$gte": datetime.utcnow() - timedelta(days=14)}
            })
            
            if recent_notification:
                continue
            
            suggestion = {
                "user_id": user_id,
                "user_email": user.get("email"),
                "user_name": user.get("name"),
                "service_name": service_name,
                "engagement_count": engagement_count,
                "questions": questions,
                "reasons": [
                    f"You've accessed {service_name} {engagement_count} times this week",
                    f"You've asked {len(questions)} different questions about this service",
                    "You might benefit from personalized assistance"
                ],
                "score": min(5, engagement_count)
            }
            
            premium_suggestions.append(suggestion)
        
        return premium_suggestions
    
    def send_premium_suggestions(self):
        """Send premium suggestions to eligible users"""
        candidates = self.analyze_premium_candidates()
        
        sent_count = 0
        for candidate in candidates:
            # Group suggestions by user
            user_suggestions = [candidate]  # Can be extended to group multiple services per user
            
            success = self.email_service.send_premium_suggestion_email(
                candidate["user_email"],
                candidate["user_name"],
                user_suggestions
            )
            
            if success:
                # Log the notification
                self.notifications_col.insert_one({
                    "user_id": candidate["user_id"],
                    "type": "premium_suggestion",
                    "sent_at": datetime.utcnow(),
                    "email": candidate["user_email"],
                    "service": candidate["service_name"],
                    "engagement_count": candidate["engagement_count"]
                })
                sent_count += 1
        
        return sent_count
    
    def generate_admin_report(self):
        """Generate weekly admin report data"""
        week_ago = datetime.utcnow() - timedelta(days=7)
        
        # Get basic metrics
        total_users = self.users_col.count_documents({})
        weekly_engagements = self.engagements_col.count_documents({
            "timestamp": {"$gte": week_ago}
        })
        
        # Get premium candidates
        premium_candidates = len(self.analyze_premium_candidates())
        
        # Get popular services
        popular_pipeline = [
            {"$match": {"timestamp": {"$gte": week_ago}}},
            {"$group": {"_id": "$service", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 5}
        ]
        
        popular_services = [
            {"name": item["_id"] or "Unknown", "count": item["count"]}
            for item in self.engagements_col.aggregate(popular_pipeline)
        ]
        
        # Get emails sent this week
        emails_sent = self.notifications_col.count_documents({
            "sent_at": {"$gte": week_ago},
            "type": "premium_suggestion"
        })
        
        return {
            "total_users": total_users,
            "weekly_engagements": weekly_engagements,
            "premium_candidates": premium_candidates,
            "popular_services": popular_services,
            "emails_sent": emails_sent
        }