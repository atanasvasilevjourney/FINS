import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Search as SearchIcon,
  FilterList as FilterIcon,
} from '@mui/icons-material';
import { DataGrid, GridColDef, GridValueGetterParams } from '@mui/x-data-grid';

// Mock data
const mockAccounts = [
  {
    id: 1,
    accountCode: '1000',
    accountName: 'Cash and Cash Equivalents',
    accountType: 'Asset',
    accountCategory: 'Current Assets',
    normalBalance: 'Debit',
    isActive: true,
    description: 'Cash on hand and in bank accounts',
  },
  {
    id: 2,
    accountCode: '1100',
    accountName: 'Accounts Receivable',
    accountType: 'Asset',
    accountCategory: 'Current Assets',
    normalBalance: 'Debit',
    isActive: true,
    description: 'Amounts owed by customers',
  },
  {
    id: 3,
    accountCode: '1200',
    accountName: 'Inventory',
    accountType: 'Asset',
    accountCategory: 'Current Assets',
    normalBalance: 'Debit',
    isActive: true,
    description: 'Goods held for sale',
  },
  {
    id: 4,
    accountCode: '2000',
    accountName: 'Accounts Payable',
    accountType: 'Liability',
    accountCategory: 'Current Liabilities',
    normalBalance: 'Credit',
    isActive: true,
    description: 'Amounts owed to suppliers',
  },
  {
    id: 5,
    accountCode: '3000',
    accountName: 'Common Stock',
    accountType: 'Equity',
    accountCategory: 'Shareholders Equity',
    normalBalance: 'Credit',
    isActive: true,
    description: 'Common stock issued',
  },
  {
    id: 6,
    accountCode: '4000',
    accountName: 'Sales Revenue',
    accountType: 'Revenue',
    accountCategory: 'Operating Revenue',
    normalBalance: 'Credit',
    isActive: true,
    description: 'Revenue from sales',
  },
  {
    id: 7,
    accountCode: '5000',
    accountName: 'Cost of Goods Sold',
    accountType: 'Expense',
    accountCategory: 'Operating Expenses',
    normalBalance: 'Debit',
    isActive: true,
    description: 'Cost of goods sold',
  },
];

const accountTypes = ['Asset', 'Liability', 'Equity', 'Revenue', 'Expense'];
const accountCategories = [
  'Current Assets',
  'Fixed Assets',
  'Current Liabilities',
  'Long-term Liabilities',
  'Shareholders Equity',
  'Operating Revenue',
  'Operating Expenses',
  'Other Income',
  'Other Expenses',
];

interface AccountFormData {
  accountCode: string;
  accountName: string;
  accountType: string;
  accountCategory: string;
  normalBalance: string;
  description: string;
}

const ChartOfAccountsPage: React.FC = () => {
  const [accounts, setAccounts] = useState(mockAccounts);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('');
  const [filterCategory, setFilterCategory] = useState('');
  const [openDialog, setOpenDialog] = useState(false);
  const [editingAccount, setEditingAccount] = useState<number | null>(null);
  const [formData, setFormData] = useState<AccountFormData>({
    accountCode: '',
    accountName: '',
    accountType: '',
    accountCategory: '',
    normalBalance: '',
    description: '',
  });

  // Filter accounts based on search and filters
  const filteredAccounts = accounts.filter((account) => {
    const matchesSearch = account.accountName.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         account.accountCode.includes(searchTerm);
    const matchesType = !filterType || account.accountType === filterType;
    const matchesCategory = !filterCategory || account.accountCategory === filterCategory;
    
    return matchesSearch && matchesType && matchesCategory;
  });

  const handleOpenDialog = (accountId?: number) => {
    if (accountId) {
      const account = accounts.find(a => a.id === accountId);
      if (account) {
        setFormData({
          accountCode: account.accountCode,
          accountName: account.accountName,
          accountType: account.accountType,
          accountCategory: account.accountCategory,
          normalBalance: account.normalBalance,
          description: account.description,
        });
        setEditingAccount(accountId);
      }
    } else {
      setFormData({
        accountCode: '',
        accountName: '',
        accountType: '',
        accountCategory: '',
        normalBalance: '',
        description: '',
      });
      setEditingAccount(null);
    }
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setEditingAccount(null);
  };

  const handleSaveAccount = () => {
    if (editingAccount) {
      // Update existing account
      setAccounts(accounts.map(account =>
        account.id === editingAccount
          ? { ...account, ...formData }
          : account
      ));
    } else {
      // Add new account
      const newAccount = {
        id: Math.max(...accounts.map(a => a.id)) + 1,
        ...formData,
        isActive: true,
      };
      setAccounts([...accounts, newAccount]);
    }
    handleCloseDialog();
  };

  const handleDeleteAccount = (accountId: number) => {
    setAccounts(accounts.map(account =>
      account.id === accountId
        ? { ...account, isActive: false }
        : account
    ));
  };

  const columns: GridColDef[] = [
    {
      field: 'accountCode',
      headerName: 'Account Code',
      width: 150,
      sortable: true,
    },
    {
      field: 'accountName',
      headerName: 'Account Name',
      width: 300,
      sortable: true,
    },
    {
      field: 'accountType',
      headerName: 'Type',
      width: 120,
      renderCell: (params) => (
        <Chip
          label={params.value}
          size="small"
          color={
            params.value === 'Asset' ? 'primary' :
            params.value === 'Liability' ? 'error' :
            params.value === 'Equity' ? 'success' :
            params.value === 'Revenue' ? 'info' : 'warning'
          }
        />
      ),
    },
    {
      field: 'accountCategory',
      headerName: 'Category',
      width: 200,
    },
    {
      field: 'normalBalance',
      headerName: 'Normal Balance',
      width: 150,
      renderCell: (params) => (
        <Chip
          label={params.value}
          size="small"
          variant="outlined"
          color={params.value === 'Debit' ? 'primary' : 'secondary'}
        />
      ),
    },
    {
      field: 'isActive',
      headerName: 'Status',
      width: 100,
      renderCell: (params) => (
        <Chip
          label={params.value ? 'Active' : 'Inactive'}
          size="small"
          color={params.value ? 'success' : 'default'}
        />
      ),
    },
    {
      field: 'actions',
      headerName: 'Actions',
      width: 120,
      sortable: false,
      renderCell: (params) => (
        <Box>
          <Tooltip title="Edit">
            <IconButton
              size="small"
              onClick={() => handleOpenDialog(params.row.id)}
            >
              <EditIcon />
            </IconButton>
          </Tooltip>
          <Tooltip title="Delete">
            <IconButton
              size="small"
              onClick={() => handleDeleteAccount(params.row.id)}
              color="error"
            >
              <DeleteIcon />
            </IconButton>
          </Tooltip>
        </Box>
      ),
    },
  ];

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">Chart of Accounts</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => handleOpenDialog()}
        >
          Add Account
        </Button>
      </Box>

      {/* Filters */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
            <TextField
              label="Search accounts"
              variant="outlined"
              size="small"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              InputProps={{
                startAdornment: <SearchIcon sx={{ mr: 1, color: 'text.secondary' }} />,
              }}
              sx={{ minWidth: 300 }}
            />
            
            <FormControl size="small" sx={{ minWidth: 150 }}>
              <InputLabel>Account Type</InputLabel>
              <Select
                value={filterType}
                label="Account Type"
                onChange={(e) => setFilterType(e.target.value)}
              >
                <MenuItem value="">All Types</MenuItem>
                {accountTypes.map((type) => (
                  <MenuItem key={type} value={type}>{type}</MenuItem>
                ))}
              </Select>
            </FormControl>

            <FormControl size="small" sx={{ minWidth: 150 }}>
              <InputLabel>Category</InputLabel>
              <Select
                value={filterCategory}
                label="Category"
                onChange={(e) => setFilterCategory(e.target.value)}
              >
                <MenuItem value="">All Categories</MenuItem>
                {accountCategories.map((category) => (
                  <MenuItem key={category} value={category}>{category}</MenuItem>
                ))}
              </Select>
            </FormControl>
          </Box>
        </CardContent>
      </Card>

      {/* Data Grid */}
      <Card>
        <CardContent>
          <DataGrid
            rows={filteredAccounts}
            columns={columns}
            pageSize={10}
            rowsPerPageOptions={[10, 25, 50]}
            disableSelectionOnClick
            autoHeight
            sx={{
              '& .MuiDataGrid-cell:focus': {
                outline: 'none',
              },
            }}
          />
        </CardContent>
      </Card>

      {/* Add/Edit Dialog */}
      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="md" fullWidth>
        <DialogTitle>
          {editingAccount ? 'Edit Account' : 'Add New Account'}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 1 }}>
            <TextField
              label="Account Code"
              value={formData.accountCode}
              onChange={(e) => setFormData({ ...formData, accountCode: e.target.value })}
              required
            />
            
            <TextField
              label="Account Name"
              value={formData.accountName}
              onChange={(e) => setFormData({ ...formData, accountName: e.target.value })}
              required
            />
            
            <FormControl>
              <InputLabel>Account Type</InputLabel>
              <Select
                value={formData.accountType}
                label="Account Type"
                onChange={(e) => setFormData({ ...formData, accountType: e.target.value })}
                required
              >
                {accountTypes.map((type) => (
                  <MenuItem key={type} value={type}>{type}</MenuItem>
                ))}
              </Select>
            </FormControl>
            
            <FormControl>
              <InputLabel>Account Category</InputLabel>
              <Select
                value={formData.accountCategory}
                label="Account Category"
                onChange={(e) => setFormData({ ...formData, accountCategory: e.target.value })}
                required
              >
                {accountCategories.map((category) => (
                  <MenuItem key={category} value={category}>{category}</MenuItem>
                ))}
              </Select>
            </FormControl>
            
            <FormControl>
              <InputLabel>Normal Balance</InputLabel>
              <Select
                value={formData.normalBalance}
                label="Normal Balance"
                onChange={(e) => setFormData({ ...formData, normalBalance: e.target.value })}
                required
              >
                <MenuItem value="Debit">Debit</MenuItem>
                <MenuItem value="Credit">Credit</MenuItem>
              </Select>
            </FormControl>
            
            <TextField
              label="Description"
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              multiline
              rows={3}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button onClick={handleSaveAccount} variant="contained">
            {editingAccount ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default ChartOfAccountsPage; 