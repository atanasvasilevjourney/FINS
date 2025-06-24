import React from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  Chip,
  LinearProgress,
  Avatar,
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  AccountBalance,
  Receipt,
  People,
  ShoppingCart,
  AttachMoney,
  Assessment,
} from '@mui/icons-material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell } from 'recharts';

// Mock data for charts
const cashFlowData = [
  { month: 'Jan', cashFlow: 45000, revenue: 52000, expenses: 7000 },
  { month: 'Feb', cashFlow: 52000, revenue: 58000, expenses: 6000 },
  { month: 'Mar', cashFlow: 48000, revenue: 55000, expenses: 7000 },
  { month: 'Apr', cashFlow: 61000, revenue: 68000, expenses: 7000 },
  { month: 'May', cashFlow: 55000, revenue: 62000, expenses: 7000 },
  { month: 'Jun', cashFlow: 67000, revenue: 74000, expenses: 7000 },
];

const agingData = [
  { name: 'Current', value: 65, color: '#4caf50' },
  { name: '1-30 Days', value: 20, color: '#ff9800' },
  { name: '31-60 Days', value: 10, color: '#f44336' },
  { name: '60+ Days', value: 5, color: '#9c27b0' },
];

const topVendors = [
  { name: 'ABC Supplies', amount: 125000, percentage: 25 },
  { name: 'XYZ Corporation', amount: 98000, percentage: 20 },
  { name: 'Tech Solutions', amount: 75000, percentage: 15 },
  { name: 'Office Plus', amount: 62000, percentage: 12 },
];

const topCustomers = [
  { name: 'Global Corp', amount: 180000, percentage: 30 },
  { name: 'Local Business', amount: 120000, percentage: 20 },
  { name: 'Startup Inc', amount: 90000, percentage: 15 },
  { name: 'Enterprise Ltd', amount: 75000, percentage: 12 },
];

const DashboardPage: React.FC = () => {
  const metrics = [
    {
      title: 'Total Revenue',
      value: '$2,450,000',
      change: '+12.5%',
      trend: 'up',
      icon: <TrendingUp />,
      color: '#4caf50',
    },
    {
      title: 'Total Expenses',
      value: '$1,850,000',
      change: '+8.2%',
      trend: 'up',
      icon: <TrendingDown />,
      color: '#f44336',
    },
    {
      title: 'Net Profit',
      value: '$600,000',
      change: '+18.3%',
      trend: 'up',
      icon: <AttachMoney />,
      color: '#2196f3',
    },
    {
      title: 'Cash Flow',
      value: '$450,000',
      change: '+15.7%',
      trend: 'up',
      icon: <AccountBalance />,
      color: '#ff9800',
    },
  ];

  const quickActions = [
    { title: 'Create Journal Entry', icon: <AccountBalance />, color: '#1976d2' },
    { title: 'Process Invoice', icon: <Receipt />, color: '#dc004e' },
    { title: 'Add Customer', icon: <People />, color: '#388e3c' },
    { title: 'Create PO', icon: <ShoppingCart />, color: '#f57c00' },
  ];

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>
      
      {/* Key Metrics */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {metrics.map((metric, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <Box>
                    <Typography color="textSecondary" gutterBottom variant="body2">
                      {metric.title}
                    </Typography>
                    <Typography variant="h5" component="div" sx={{ fontWeight: 'bold' }}>
                      {metric.value}
                    </Typography>
                    <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                      <Chip
                        label={metric.change}
                        size="small"
                        color={metric.trend === 'up' ? 'success' : 'error'}
                        sx={{ mr: 1 }}
                      />
                      <Typography variant="body2" color="textSecondary">
                        vs last month
                      </Typography>
                    </Box>
                  </Box>
                  <Avatar sx={{ bgcolor: metric.color, width: 56, height: 56 }}>
                    {metric.icon}
                  </Avatar>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Charts Section */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {/* Cash Flow Chart */}
        <Grid item xs={12} lg={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Cash Flow Overview
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={cashFlowData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis />
                  <Tooltip />
                  <Line type="monotone" dataKey="cashFlow" stroke="#2196f3" strokeWidth={2} />
                  <Line type="monotone" dataKey="revenue" stroke="#4caf50" strokeWidth={2} />
                  <Line type="monotone" dataKey="expenses" stroke="#f44336" strokeWidth={2} />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Aging Analysis */}
        <Grid item xs={12} lg={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Accounts Receivable Aging
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={agingData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={100}
                    paddingAngle={5}
                    dataKey="value"
                  >
                    {agingData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
              <Box sx={{ mt: 2 }}>
                {agingData.map((item, index) => (
                  <Box key={index} sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    <Box
                      sx={{
                        width: 12,
                        height: 12,
                        borderRadius: '50%',
                        bgcolor: item.color,
                        mr: 1,
                      }}
                    />
                    <Typography variant="body2" sx={{ flexGrow: 1 }}>
                      {item.name}
                    </Typography>
                    <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
                      {item.value}%
                    </Typography>
                  </Box>
                ))}
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Top Vendors and Customers */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {/* Top Vendors */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Top Vendors (This Month)
              </Typography>
              {topVendors.map((vendor, index) => (
                <Box key={index} sx={{ mb: 2 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                    <Typography variant="body2">{vendor.name}</Typography>
                    <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
                      ${vendor.amount.toLocaleString()}
                    </Typography>
                  </Box>
                  <LinearProgress
                    variant="determinate"
                    value={vendor.percentage}
                    sx={{ height: 8, borderRadius: 4 }}
                  />
                </Box>
              ))}
            </CardContent>
          </Card>
        </Grid>

        {/* Top Customers */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Top Customers (This Month)
              </Typography>
              {topCustomers.map((customer, index) => (
                <Box key={index} sx={{ mb: 2 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                    <Typography variant="body2">{customer.name}</Typography>
                    <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
                      ${customer.amount.toLocaleString()}
                    </Typography>
                  </Box>
                  <LinearProgress
                    variant="determinate"
                    value={customer.percentage}
                    sx={{ height: 8, borderRadius: 4 }}
                  />
                </Box>
              ))}
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Quick Actions */}
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Quick Actions
              </Typography>
              <Grid container spacing={2}>
                {quickActions.map((action, index) => (
                  <Grid item xs={6} sm={3} key={index}>
                    <Box
                      sx={{
                        p: 2,
                        border: 1,
                        borderColor: 'divider',
                        borderRadius: 2,
                        textAlign: 'center',
                        cursor: 'pointer',
                        '&:hover': {
                          bgcolor: 'action.hover',
                        },
                      }}
                    >
                      <Avatar sx={{ bgcolor: action.color, width: 48, height: 48, mx: 'auto', mb: 1 }}>
                        {action.icon}
                      </Avatar>
                      <Typography variant="body2">{action.title}</Typography>
                    </Box>
                  </Grid>
                ))}
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default DashboardPage; 