from flask import Flask, render_template, request, jsonify, redirect
import uuid
from datetime import datetime
import random
import re
import string

app = Flask(__name__)

# Store proposals and short URLs in memory (in production, use a database)
proposals = {}
url_mappings = {}

# Configuration
BASE_URL = "https://your-domain.com"  # Replace with your actual domain
SHORT_URL_LENGTH = 6

def generate_short_code():
    """Generate a random short code for URLs"""
    characters = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choices(characters, k=SHORT_URL_LENGTH))
        if code not in url_mappings:
            return code

def generate_love_message(receiver_name):
    # [Previous message generation code remains the same]
    intros = [
        f"My dearest {receiver_name},",
        f"Dear {receiver_name},",
        f"To my amazing {receiver_name},",
        f"My beloved {receiver_name},",
        f"My sweetest {receiver_name},",
        f"To the one who holds my heart, {receiver_name},",
        f"My love, {receiver_name},"
    ]
    
    middles = [
        "From the moment I first saw you, you've captured my heart in ways I never thought possible. Your smile lights up my world, and your laugh is the sweetest melody I've ever heard.",
        "Every moment spent with you feels like a beautiful dream I never want to wake up from. You make my heart skip a beat with just a simple glance.",
        "You bring colors to my world that I never knew existed. Your presence in my life makes everything brighter, better, and more beautiful.",
        "Loving you feels as natural as breathing. You are the rhythm to my heart, the melody to my song, and the light in my darkest days.",
        "I never believed in fairy tales until you walked into my life and made every moment feel magical. With you, even the ordinary becomes extraordinary.",
        "The way your eyes sparkle when you laugh and the warmth of your embrace make me fall in love with you over and over again.",
        "There's a magic in the way you make me feel—like I'm the luckiest person in the world just because I get to love you."
    ]
    
    feelings = [
        "The way you understand me, support me, and care for me makes every day feel like Valentine's Day. Your presence in my life is the greatest gift I could ever ask for.",
        "My heart beats a little faster whenever I think of you. You've become such an important part of my life that I can't imagine a single day without you.",
        "The warmth of your love and the tenderness of your heart make me fall for you more and more each day. You're everything I've ever dreamed of and more.",
        "Loving you is the easiest thing I've ever done. Your love is my comfort, my joy, and my greatest adventure.",
        "No matter where life takes us, as long as I have you by my side, I know I'll always be home.",
        "Your kindness, your strength, your laughter—they make my world infinitely better. I cherish every single thing about you.",
        "I love the way you make my heart feel safe and my soul feel alive. You are my greatest love, my best friend, and my forever."
    ]
    
    endings = [
        "Will you be my Valentine and let me show you just how special you are to me?",
        "Would you make me the happiest person by being my Valentine?",
        "I can't think of anyone else I'd rather spend Valentine's Day with. Will you be mine?",
        "All I want is to hold your hand, look into your eyes, and tell you just how much you mean to me. Will you let me be yours, today and always?",
        "No matter what day it is, my heart belongs to you. But today, I'd love nothing more than to call you my Valentine.",
        "Every love story is special, but ours is my favorite. Would you do me the honor of being my Valentine?",
        "With all my heart, with all my soul, I choose you—today, tomorrow, and always. Will you be mine?"
    ]
    
    message = f"{random.choice(intros)}\n\n{random.choice(middles)}\n\n{random.choice(feelings)}\n\n{random.choice(endings)}"
    return message

@app.route('/')
def home():
    return render_template('create.html')

@app.route('/create', methods=['POST'])
def create():
    try:
        sender_name = request.form['sender_name']
        receiver_name = request.form['receiver_name']
        phone_number = request.form.get('phone_number', '').strip()
        
        # Generate the message
        message = generate_love_message(receiver_name)
        
        # Generate proposal ID and short URL
        proposal_id = str(uuid.uuid4())
        short_code = generate_short_code()
        
        # Store proposal
        proposals[proposal_id] = {
            'sender_name': sender_name,
            'receiver_name': receiver_name,
            'message': message,
            'phone_number': phone_number,
            'created_at': datetime.now().isoformat()
        }
        
        # Store URL mapping
        url_mappings[short_code] = proposal_id
        
        # Return short URL
        short_url = f"{BASE_URL}/{short_code}"
        return jsonify({'link': short_url})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/<short_code>')
def redirect_to_proposal(short_code):
    proposal_id = url_mappings.get(short_code)
    if not proposal_id:
        return "Proposal not found", 404
    
    proposal = proposals.get(proposal_id)
    if not proposal:
        return "Proposal not found", 404
    
    return render_template('proposal.html', 
                         receiver_name=proposal['receiver_name'],
                         sender_name=proposal['sender_name'],
                         message=proposal['message'],
                         phone_number=proposal['phone_number'])

if __name__ == '__main__':
    app.run(debug=True)