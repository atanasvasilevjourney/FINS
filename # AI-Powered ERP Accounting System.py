# ... existing code ...
# from ai.agent import AIAgent  # Removed AI integration
from accounting.core import AccountingEngine
from security.encryption import AESEncryption
from ui.dashboard import DashboardManager
# ... existing code ...
class ERPSystem:
    def __init__(self):
        self.accounting_engine = AccountingEngine()
        # self.ai_agent = AIAgent()  # Removed AI integration
        self.encryption = AESEncryption()
        self.dashboard = DashboardManager()
        
        # Initialize system components
        self.initialize_components()
        
    def initialize_components(self):
        """Initialize all core system components"""
        # Set up database connections
        self.setup_databases()
        
        # Initialize AI models
        # self.ai_agent.load_models()  # Removed AI integration
        
        # Set up security protocols
        self.setup_security()
# ... existing code ... 