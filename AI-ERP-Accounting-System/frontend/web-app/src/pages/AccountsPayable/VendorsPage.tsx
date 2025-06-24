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
  Grid,
  Avatar,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Search as SearchIcon,
  Business as BusinessIcon,
  Phone as PhoneIcon,
  Email as EmailIcon,
  LocationOn as LocationIcon,
} from '@mui/icons-material';
import { DataGrid, GridColDef } from '@mui/x-data-grid';

// Mock data
const mockVendors = [
  {
    id: 1,
    vendorCode: 'V001',
    name: 'ABC Supplies Inc.',
    contactPerson: 'John Smith',
    email: 'john.smith@abcsupplies.com',
    phone: '+1 (555) 123-4567',
    address: '123 Business St, New York, NY 10001',
    taxId: '12-3456789',
    paymentTerms: 'Net 30',
    creditLimit: 50000,
    status: 'Active',
    category: 'Office Supplies',
    rating: 4.5,
  },
  {
    id: 2,
    vendorCode: 'V002',
    name: 'XYZ Corporation',
    contactPerson: 'Jane Doe',
    email: 'jane.doe@xyzcorp.com',
    phone: '+1 (555) 987-6543',
    address: '456 Corporate Ave, Los Angeles, CA 90210',
    taxId: '98-7654321',
    paymentTerms: 'Net 45',
    creditLimit: 75000,
    status: 'Active',
    category: 'Technology',
    rating: 4.8,
  },
  {
    id: 3,
    vendorCode: 'V003',
    name: 'Tech Solutions Ltd.',
    contactPerson: 'Mike Johnson',
    email: 'mike.johnson@techsolutions.com',
    phone: '+1 (555) 456-7890',
    address: '789 Tech Blvd, San Francisco, CA 94105',
    taxId: '45-6789012',
    paymentTerms: 'Net 30',
    creditLimit: 100000,
    status: 'Active',
    category: 'Technology',
    rating: 4.2,
  },
  {
    id: 4,
    vendorCode: 'V004',
    name: 'Office Plus Co.',
    contactPerson: 'Sarah Wilson',
    email: 'sarah.wilson@officeplus.com',
    phone: '+1 (555) 321-0987',
    address: '321 Office Park, Chicago, IL 60601',
    taxId: '32-1098765',
    paymentTerms: 'Net 15',
    creditLimit: 25000,
    status: 'Inactive',
    category: 'Office Supplies',
    rating: 3.9,
  },
];

const vendorCategories = [
  'Office Supplies',
  'Technology',
  'Manufacturing',
  'Services',
  'Transportation',
  'Utilities',
  'Other',
];

const paymentTerms = [
  'Net 15',
  'Net 30',
  'Net 45',
  'Net 60',
  'Due on Receipt',
];

interface VendorFormData {
  vendorCode: string;
  name: string;
  contactPerson: string;
  email: string;
  phone: string;
  address: string;
  taxId: string;
  paymentTerms: string;
  creditLimit: number;
  category: string;
}

const VendorsPage: React.FC = () => {
  const [vendors, setVendors] = useState(mockVendors);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterCategory, setFilterCategory] = useState('');
  const [filterStatus, setFilterStatus] = useState('');
  const [openDialog, setOpenDialog] = useState(false);
  const [editingVendor, setEditingVendor] = useState<number | null>(null);
  const [formData, setFormData] = useState<VendorFormData>({
    vendorCode: '',
    name: '',
    contactPerson: '',
    email: '',
    phone: '',
    address: '',
    taxId: '',
    paymentTerms: '',
    creditLimit: 0,
    category: '',
  });

  // Filter vendors based on search and filters
  const filteredVendors = vendors.filter((vendor) => {
    const matchesSearch = vendor.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         vendor.vendorCode.includes(searchTerm) ||
                         vendor.contactPerson.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = !filterCategory || vendor.category === filterCategory;
    const matchesStatus = !filterStatus || vendor.status === filterStatus;
    
    return matchesSearch && matchesCategory && matchesStatus;
  });

  const handleOpenDialog = (vendorId?: number) => {
    if (vendorId) {
      const vendor = vendors.find(v => v.id === vendorId);
      if (vendor) {
        setFormData({
          vendorCode: vendor.vendorCode,
          name: vendor.name,
          contactPerson: vendor.contactPerson,
          email: vendor.email,
          phone: vendor.phone,
          address: vendor.address,
          taxId: vendor.taxId,
          paymentTerms: vendor.paymentTerms,
          creditLimit: vendor.creditLimit,
          category: vendor.category,
        });
        setEditingVendor(vendorId);
      }
    } else {
      setFormData({
        vendorCode: '',
        name: '',
        contactPerson: '',
        email: '',
        phone: '',
        address: '',
        taxId: '',
        paymentTerms: '',
        creditLimit: 0,
        category: '',
      });
      setEditingVendor(null);
    }
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setEditingVendor(null);
  };

  const handleSaveVendor = () => {
    if (editingVendor) {
      // Update existing vendor
      setVendors(vendors.map(vendor =>
        vendor.id === editingVendor
          ? { ...vendor, ...formData }
          : vendor
      ));
    } else {
      // Add new vendor
      const newVendor = {
        id: Math.max(...vendors.map(v => v.id)) + 1,
        ...formData,
        status: 'Active',
        rating: 0,
      };
      setVendors([...vendors, newVendor]);
    }
    handleCloseDialog();
  };

  const handleDeleteVendor = (vendorId: number) => {
    setVendors(vendors.map(vendor =>
      vendor.id === vendorId
        ? { ...vendor, status: 'Inactive' }
        : vendor
    ));
  };

  const columns: GridColDef[] = [
    {
      field: 'vendorCode',
      headerName: 'Vendor Code',
      width: 120,
    },
    {
      field: 'name',
      headerName: 'Vendor Name',
      width: 250,
      renderCell: (params) => (
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <Avatar sx={{ width: 32, height: 32, mr: 1, bgcolor: 'primary.main' }}>
            <BusinessIcon />
          </Avatar>
          <Typography variant="body2">{params.value}</Typography>
        </Box>
      ),
    },
    {
      field: 'contactPerson',
      headerName: 'Contact Person',
      width: 150,
    },
    {
      field: 'email',
      headerName: 'Email',
      width: 200,
      renderCell: (params) => (
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <EmailIcon sx={{ mr: 0.5, fontSize: 16 }} />
          <Typography variant="body2">{params.value}</Typography>
        </Box>
      ),
    },
    {
      field: 'phone',
      headerName: 'Phone',
      width: 150,
      renderCell: (params) => (
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <PhoneIcon sx={{ mr: 0.5, fontSize: 16 }} />
          <Typography variant="body2">{params.value}</Typography>
        </Box>
      ),
    },
    {
      field: 'category',
      headerName: 'Category',
      width: 150,
      renderCell: (params) => (
        <Chip label={params.value} size="small" variant="outlined" />
      ),
    },
    {
      field: 'paymentTerms',
      headerName: 'Payment Terms',
      width: 120,
    },
    {
      field: 'creditLimit',
      headerName: 'Credit Limit',
      width: 120,
      renderCell: (params) => (
        <Typography variant="body2">
          ${params.value.toLocaleString()}
        </Typography>
      ),
    },
    {
      field: 'status',
      headerName: 'Status',
      width: 100,
      renderCell: (params) => (
        <Chip
          label={params.value}
          size="small"
          color={params.value === 'Active' ? 'success' : 'default'}
        />
      ),
    },
    {
      field: 'rating',
      headerName: 'Rating',
      width: 100,
      renderCell: (params) => (
        <Chip
          label={`${params.value}/5`}
          size="small"
          color={params.value >= 4 ? 'success' : params.value >= 3 ? 'warning' : 'error'}
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
              onClick={() => handleDeleteVendor(params.row.id)}
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
        <Typography variant="h4">Vendors</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => handleOpenDialog()}
        >
          Add Vendor
        </Button>
      </Box>

      {/* Filters */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} md={4}>
              <TextField
                label="Search vendors"
                variant="outlined"
                size="small"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                InputProps={{
                  startAdornment: <SearchIcon sx={{ mr: 1, color: 'text.secondary' }} />,
                }}
                fullWidth
              />
            </Grid>
            
            <Grid item xs={12} md={3}>
              <FormControl size="small" fullWidth>
                <InputLabel>Category</InputLabel>
                <Select
                  value={filterCategory}
                  label="Category"
                  onChange={(e) => setFilterCategory(e.target.value)}
                >
                  <MenuItem value="">All Categories</MenuItem>
                  {vendorCategories.map((category) => (
                    <MenuItem key={category} value={category}>{category}</MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>

            <Grid item xs={12} md={3}>
              <FormControl size="small" fullWidth>
                <InputLabel>Status</InputLabel>
                <Select
                  value={filterStatus}
                  label="Status"
                  onChange={(e) => setFilterStatus(e.target.value)}
                >
                  <MenuItem value="">All Status</MenuItem>
                  <MenuItem value="Active">Active</MenuItem>
                  <MenuItem value="Inactive">Inactive</MenuItem>
                </Select>
              </FormControl>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Data Grid */}
      <Card>
        <CardContent>
          <DataGrid
            rows={filteredVendors}
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
          {editingVendor ? 'Edit Vendor' : 'Add New Vendor'}
        </DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12} md={6}>
              <TextField
                label="Vendor Code"
                value={formData.vendorCode}
                onChange={(e) => setFormData({ ...formData, vendorCode: e.target.value })}
                required
                fullWidth
              />
            </Grid>
            
            <Grid item xs={12} md={6}>
              <TextField
                label="Vendor Name"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                required
                fullWidth
              />
            </Grid>
            
            <Grid item xs={12} md={6}>
              <TextField
                label="Contact Person"
                value={formData.contactPerson}
                onChange={(e) => setFormData({ ...formData, contactPerson: e.target.value })}
                required
                fullWidth
              />
            </Grid>
            
            <Grid item xs={12} md={6}>
              <TextField
                label="Email"
                type="email"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                required
                fullWidth
              />
            </Grid>
            
            <Grid item xs={12} md={6}>
              <TextField
                label="Phone"
                value={formData.phone}
                onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                required
                fullWidth
              />
            </Grid>
            
            <Grid item xs={12} md={6}>
              <TextField
                label="Tax ID"
                value={formData.taxId}
                onChange={(e) => setFormData({ ...formData, taxId: e.target.value })}
                fullWidth
              />
            </Grid>
            
            <Grid item xs={12} md={6}>
              <FormControl fullWidth>
                <InputLabel>Category</InputLabel>
                <Select
                  value={formData.category}
                  label="Category"
                  onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                  required
                >
                  {vendorCategories.map((category) => (
                    <MenuItem key={category} value={category}>{category}</MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            
            <Grid item xs={12} md={6}>
              <FormControl fullWidth>
                <InputLabel>Payment Terms</InputLabel>
                <Select
                  value={formData.paymentTerms}
                  label="Payment Terms"
                  onChange={(e) => setFormData({ ...formData, paymentTerms: e.target.value })}
                  required
                >
                  {paymentTerms.map((term) => (
                    <MenuItem key={term} value={term}>{term}</MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            
            <Grid item xs={12} md={6}>
              <TextField
                label="Credit Limit"
                type="number"
                value={formData.creditLimit}
                onChange={(e) => setFormData({ ...formData, creditLimit: Number(e.target.value) })}
                fullWidth
              />
            </Grid>
            
            <Grid item xs={12}>
              <TextField
                label="Address"
                value={formData.address}
                onChange={(e) => setFormData({ ...formData, address: e.target.value })}
                multiline
                rows={3}
                fullWidth
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button onClick={handleSaveVendor} variant="contained">
            {editingVendor ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default VendorsPage; 