#!/usr/bin/env python3
"""
Debug OpenAI quota issues - helps identify why quota errors occur
when dashboard shows available quota.
"""

import os
from openai import OpenAI

def check_quota_issue():
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("❌ OPENAI_API_KEY environment variable not set!")
        return
    
    print("="*70)
    print("OpenAI API Quota Diagnostic")
    print("="*70)
    print()
    print(f"API Key (first/last 4 chars): {api_key[:7]}...{api_key[-4:]}")
    print()
    
    client = OpenAI(api_key=api_key)
    
    # Test different models
    models_to_test = [
        ('gpt-3.5-turbo', 'Cheapest, usually has highest quota'),
        ('gpt-4o-mini', 'Low-cost GPT-4 variant'),
        ('gpt-4o', 'Full GPT-4 model'),
        ('gpt-4', 'Original GPT-4'),
    ]
    
    print("Testing different models to identify quota issue...")
    print()
    
    for model, description in models_to_test:
        print(f"Testing {model} ({description})...")
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{'role': 'user', 'content': 'test'}],
                max_tokens=5
            )
            print(f"  ✅ {model}: SUCCESS")
        except Exception as e:
            error_str = str(e)
            if 'quota' in error_str.lower() or 'insufficient_quota' in error_str.lower():
                print(f"  ❌ {model}: QUOTA ERROR")
                if '429' in error_str:
                    print(f"     This is a rate limit OR quota issue")
            elif 'rate_limit' in error_str.lower() or '429' in error_str:
                print(f"  ⚠️  {model}: RATE LIMIT (temporary, will work later)")
            else:
                print(f"  ❌ {model}: {error_str[:100]}")
        print()
    
    print("="*70)
    print("Common Causes & Solutions:")
    print("="*70)
    print()
    print("1. ORGANIZATION vs PERSONAL ACCOUNT")
    print("   - Check the dropdown in top-right of OpenAI dashboard")
    print("   - You might be looking at one account but using key from another")
    print("   - Solution: Make sure API key matches the account you're viewing")
    print()
    print("2. MODEL-SPECIFIC QUOTAS")
    print("   - GPT-4 has separate quotas from GPT-3.5")
    print("   - Dashboard might show GPT-3.5 quota but you're using GPT-4")
    print("   - Solution: Check quota for specific model you're using")
    print()
    print("3. DIFFERENT API KEY")
    print("   - The key in your environment might be different from dashboard")
    print("   - Solution: Compare first/last 4 chars shown above with dashboard")
    print()
    print("4. BILLING/Payment Method")
    print("   - Account might need payment method even if quota shows")
    print("   - Solution: Add payment method at https://platform.openai.com/account/billing")
    print()
    print("5. RATE LIMITS (not quota)")
    print("   - You might be hitting requests-per-minute limits")
    print("   - Solution: Add delays between requests or reduce concurrency")
    print()
    print("="*70)
    print("Next Steps:")
    print("="*70)
    print("1. Go to: https://platform.openai.com/api-keys")
    print("   - Find the key that matches: {api_key[:7]}...{api_key[-4:]}")
    print("   - Check which organization it belongs to")
    print()
    print("2. Go to: https://platform.openai.com/usage")
    print("   - Check usage for the organization your key belongs to")
    print("   - Look at model-specific quotas")
    print()
    print("3. Check organization dropdown (top-right)")
    print("   - Make sure you're viewing the same org as your API key")
    print()
    print("4. If using GPT-4, check GPT-4 specific quota:")
    print("   - https://platform.openai.com/account/limits")
    print("   - GPT-4 often has separate, lower limits")
    print()

if __name__ == "__main__":
    check_quota_issue()


