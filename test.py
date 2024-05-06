from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        """Set up before every test"""

        self.client = app.test_client()
        app.config['TESTING'] = True

    
    def test_homepage(self):
        """Test session information and HTML"""

        with self.client:
            response = self.client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIn(b'High Score:', response.data)
            self.assertIn(b'Score:', response.data)
            self.assertIn(b'Seconds Left', response.data)

    def test_word_validation(self):
        """Test if a word can be validated by the board"""

        with self.client as client:
            with client.session_transaction() as s:
                s['board']=[["P","E","T","A","L"],
                            ["P","E","T","A","L"],
                            ["P","E","T","A","L"],
                            ["P","E","T","A","L"],
                            ["P","E","T","A","L"]]
        response = self.client.get('/submit-guess?guess=pet')
        self.assertEqual(response.json['result'], 'ok')

    def test_existing_word(self):
        """test is the word is in the dictionary"""

        self.client.get('/')
        response = self.client.get('/submit-guess?guess=IIIIIIIIIIIIIIIIIIIILLLLLLLLLLLLMMMMBBB')
        self.assertEqual(response.json['result'], "not-word")

    
    def test_word_on_board(self):
        """Test if the word is on the board"""
        self.client.get('/')
        response = self.client.get('/submit-guess?guess=impossible')
        self.assertEqual(response.json['result'], 'not-on-board')