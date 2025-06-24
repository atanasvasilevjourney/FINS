import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { CssBaseline, Box } from '@mui/material';
import { QueryClient, QueryClientProvider } from 'react-query';
import { Provider } from 'react-redux';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';

// Store and Redux
import { store } from './store/store';

// Components
import Layout from './components/Layout/Layout';
import ProtectedRoute from './components/Auth/ProtectedRoute';
import LoginPage from './pages/Auth/LoginPage';
import DashboardPage from './pages/Dashboard/DashboardPage';

// General Ledger Pages
import ChartOfAccountsPage from './pages/GeneralLedger/ChartOfAccountsPage';
import JournalEntriesPage from './pages/GeneralLedger/JournalEntriesPage';
import FinancialStatementsPage from './pages/GeneralLedger/FinancialStatementsPage';

// Accounts Payable Pages
import VendorsPage from './pages/AccountsPayable/VendorsPage';
import APInvoicesPage from './pages/AccountsPayable/InvoicesPage';
import PaymentsPage from './pages/AccountsPayable/PaymentsPage';
import PurchaseOrdersPage from './pages/AccountsPayable/PurchaseOrdersPage';

// Accounts Receivable Pages
import CustomersPage from './pages/AccountsReceivable/CustomersPage';
import ARInvoicesPage from './pages/AccountsReceivable/InvoicesPage';
import CollectionsPage from './pages/AccountsReceivable/CollectionsPage';
import SalesOrdersPage from './pages/AccountsReceivable/SalesOrdersPage';

// Procurement Pages
import SuppliersPage from './pages/Procurement/SuppliersPage';
import PurchaseRequisitionsPage from './pages/Procurement/PurchaseRequisitionsPage';
import RFQsPage from './pages/Procurement/RFQsPage';
import ContractsPage from './pages/Procurement/ContractsPage';

// Reports Pages
import ReportsPage from './pages/Reports/ReportsPage';
import AnalyticsPage from './pages/Reports/AnalyticsPage';

// Settings Pages
import SettingsPage from './pages/Settings/SettingsPage';
import UserManagementPage from './pages/Settings/UserManagementPage';

// Create theme
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
      light: '#42a5f5',
      dark: '#1565c0',
    },
    secondary: {
      main: '#dc004e',
      light: '#ff5983',
      dark: '#9a0036',
    },
    background: {
      default: '#f5f5f5',
      paper: '#ffffff',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontSize: '2.5rem',
      fontWeight: 600,
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 600,
    },
    h3: {
      fontSize: '1.75rem',
      fontWeight: 600,
    },
    h4: {
      fontSize: '1.5rem',
      fontWeight: 600,
    },
    h5: {
      fontSize: '1.25rem',
      fontWeight: 600,
    },
    h6: {
      fontSize: '1rem',
      fontWeight: 600,
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          borderRadius: 8,
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: 12,
        },
      },
    },
  },
});

// Create React Query client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
});

function App() {
  return (
    <Provider store={store}>
      <QueryClientProvider client={queryClient}>
        <ThemeProvider theme={theme}>
          <LocalizationProvider dateAdapter={AdapterDateFns}>
            <CssBaseline />
            <Router>
              <Box sx={{ display: 'flex', minHeight: '100vh' }}>
                <Routes>
                  {/* Public routes */}
                  <Route path="/login" element={<LoginPage />} />
                  
                  {/* Protected routes */}
                  <Route path="/" element={
                    <ProtectedRoute>
                      <Layout />
                    </ProtectedRoute>
                  }>
                    {/* Dashboard */}
                    <Route index element={<Navigate to="/dashboard" replace />} />
                    <Route path="dashboard" element={<DashboardPage />} />
                    
                    {/* General Ledger */}
                    <Route path="general-ledger">
                      <Route path="chart-of-accounts" element={<ChartOfAccountsPage />} />
                      <Route path="journal-entries" element={<JournalEntriesPage />} />
                      <Route path="financial-statements" element={<FinancialStatementsPage />} />
                    </Route>
                    
                    {/* Accounts Payable */}
                    <Route path="accounts-payable">
                      <Route path="vendors" element={<VendorsPage />} />
                      <Route path="invoices" element={<APInvoicesPage />} />
                      <Route path="payments" element={<PaymentsPage />} />
                      <Route path="purchase-orders" element={<PurchaseOrdersPage />} />
                    </Route>
                    
                    {/* Accounts Receivable */}
                    <Route path="accounts-receivable">
                      <Route path="customers" element={<CustomersPage />} />
                      <Route path="invoices" element={<ARInvoicesPage />} />
                      <Route path="collections" element={<CollectionsPage />} />
                      <Route path="sales-orders" element={<SalesOrdersPage />} />
                    </Route>
                    
                    {/* Procurement */}
                    <Route path="procurement">
                      <Route path="suppliers" element={<SuppliersPage />} />
                      <Route path="purchase-requisitions" element={<PurchaseRequisitionsPage />} />
                      <Route path="rfqs" element={<RFQsPage />} />
                      <Route path="contracts" element={<ContractsPage />} />
                    </Route>
                    
                    {/* Reports */}
                    <Route path="reports">
                      <Route index element={<ReportsPage />} />
                      <Route path="analytics" element={<AnalyticsPage />} />
                    </Route>
                    
                    {/* Settings */}
                    <Route path="settings">
                      <Route index element={<SettingsPage />} />
                      <Route path="users" element={<UserManagementPage />} />
                    </Route>
                  </Route>
                  
                  {/* Catch all route */}
                  <Route path="*" element={<Navigate to="/dashboard" replace />} />
                </Routes>
              </Box>
            </Router>
          </LocalizationProvider>
        </ThemeProvider>
      </QueryClientProvider>
    </Provider>
  );
}

export default App; 