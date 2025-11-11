#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from tutorial.forms import Contact, User, SequenceForm

def test_contact_form():
    """Test Contact form validation."""
    print("Testing Contact form...")

    # Valid data
    schema = Contact()
    try:
        result = schema.deserialize({  # type: ignore[attr-defined]
            'name': 'John Doe',
            'email': 'john@example.com',
            'message': 'This is a test message with enough length.'
        })
        print("✓ Contact form valid data passed")
    except Exception as e:
        print(f"✗ Contact form valid data failed: {e}")
        return False

    # Invalid email
    try:
        result = schema.deserialize({  # type: ignore[attr-defined]
            'name': 'John Doe',
            'email': 'invalid-email',
            'message': 'This is a test message with enough length.'
        })
        print("✗ Contact form should have failed with invalid email")
        return False
    except Exception as e:
        print("✓ Contact form correctly rejected invalid email")

    # Short message
    try:
        result = schema.deserialize({  # type: ignore[attr-defined]
            'name': 'John Doe',
            'email': 'john@example.com',
            'message': 'Short'
        })
        print("✗ Contact form should have failed with short message")
        return False
    except Exception as e:
        print("✓ Contact form correctly rejected short message")

    return True

def test_user_form():
    """Test User form validation."""
    print("Testing User form...")

    # Valid data
    schema = User()
    try:
        result = schema.deserialize({  # type: ignore[attr-defined]
            'name': 'Jane Doe',
            'age': 25,
            'email': 'jane@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'interests': ['sports', 'reading'],
            'country': 'us',
            'bio': 'I am a test user.',
            'newsletter': True
        })
        print("✓ User form valid data passed")
    except Exception as e:
        print(f"✗ User form valid data failed: {e}")
        return False

    # Password mismatch
    try:
        result = schema.deserialize({  # type: ignore[attr-defined]
            'name': 'Jane Doe',
            'age': 25,
            'email': 'jane@example.com',
            'password': 'password123',
            'confirm_password': 'different',
            'interests': ['sports'],
            'country': 'us',
            'bio': '',
            'newsletter': False
        })
        print("✗ User form should have failed with password mismatch")
        return False
    except Exception as e:
        print("✓ User form correctly rejected password mismatch")

    # Age too low
    try:
        result = schema.deserialize({  # type: ignore[attr-defined]
            'name': 'Jane Doe',
            'age': 10,
            'email': 'jane@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'interests': ['sports'],
            'country': 'us',
            'bio': '',
            'newsletter': False
        })
        print("✗ User form should have failed with age too low")
        return False
    except Exception as e:
        print("✓ User form correctly rejected low age")

    return True

def test_sequence_form():
    """Test SequenceForm validation."""
    print("Testing SequenceForm...")

    schema = SequenceForm()
    try:
        result = schema.deserialize({  # type: ignore[attr-defined]
            'title': 'Test Form',
            'items': [
                {'name': 'Item 1', 'value': 10},
                {'name': 'Item 2', 'value': 20}
            ]
        })
        print("✓ SequenceForm valid data passed")
    except Exception as e:
        print(f"✗ SequenceForm valid data failed: {e}")
        return False

    # Too few items
    try:
        result = schema.deserialize({  # type: ignore[attr-defined]
            'title': 'Test Form',
            'items': []
        })
        print("✗ SequenceForm should have failed with too few items")
        return False
    except Exception as e:
        print("✓ SequenceForm correctly rejected too few items")

    return True

if __name__ == '__main__':
    print("Running thorough form validation tests...\n")

    success = True
    success &= test_contact_form()
    print()
    success &= test_user_form()
    print()
    success &= test_sequence_form()

    if success:
        print("\n✓ All form validation tests passed!")
        sys.exit(0)
    else:
        print("\n✗ Some form validation tests failed!")
        sys.exit(1)
