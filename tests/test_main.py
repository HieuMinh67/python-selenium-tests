from main import run_chrome, run_firefox

def test_chrome():
    assert run_chrome() == 'https://www.google.com'
    
def test_firefox():
    assert run_firefox() == 'https://www.google.com'
    