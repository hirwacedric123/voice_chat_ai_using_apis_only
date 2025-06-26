from django.core.management.base import BaseCommand
from django.conf import settings
import openai
import os
from dotenv import load_dotenv

class Command(BaseCommand):
    help = 'Test OpenAI API key configuration'

    def handle(self, *args, **options):
        self.stdout.write("🔍 Testing OpenAI API Key Configuration")
        self.stdout.write("=" * 50)
        
        # Check .env file
        env_exists = os.path.exists('.env')
        self.stdout.write(f"1. .env file exists: {env_exists}")
        
        # Load .env with override
        load_dotenv(override=True)
        
        # Check API key from settings
        api_key = settings.OPENAI_API_KEY
        self.stdout.write(f"2. API key from Django settings: {'✅ Found' if api_key else '❌ Not found'}")
        
        if api_key:
            self.stdout.write(f"   - Starts with 'sk-': {api_key.startswith('sk-')}")
            self.stdout.write(f"   - Length: {len(api_key)} characters")
            self.stdout.write(f"   - First 10 chars: {api_key[:10]}...")
        
        # Test the API key by making a simple request
        if api_key:
            self.stdout.write("\n3. Testing API key with OpenAI...")
            try:
                client = openai.OpenAI(api_key=api_key)
                
                # Try to list available models (this is a lightweight test)
                models = client.models.list()
                self.stdout.write("   ✅ API key is valid! Successfully connected to OpenAI")
                self.stdout.write(f"   📊 Available models count: {len(models.data)}")
                
            except openai.AuthenticationError as e:
                self.stdout.write(f"   ❌ Authentication failed: {e}")
                self.stdout.write("   💡 This means your API key is invalid or expired")
            except Exception as e:
                self.stdout.write(f"   ⚠️  Other error: {e}")
                # Try a simpler test - just create the client
                try:
                    client = openai.OpenAI(api_key=api_key)
                    self.stdout.write("   ✅ OpenAI client created successfully")
                except Exception as e2:
                    self.stdout.write(f"   ❌ Cannot create OpenAI client: {e2}")
        else:
            self.stdout.write("\n3. ❌ Cannot test API key - not configured")
        
        self.stdout.write("\n🎯 Next steps:")
        if api_key and api_key.startswith('sk-'):
            self.stdout.write("   - Your API key format looks correct")
            self.stdout.write("   - If authentication failed, check if the key is valid on OpenAI platform")
            self.stdout.write("   - Make sure your OpenAI account has sufficient credits")
        else:
            self.stdout.write("   - Please check your .env file")
            self.stdout.write("   - Ensure it contains: OPENAI_API_KEY=sk-your-key-here")
            self.stdout.write("   - Restart the Django server after making changes") 