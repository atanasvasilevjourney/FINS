import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import {
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Collapse,
  Box,
  Typography,
  Divider,
} from '@mui/material';
import {
  Dashboard,
  AccountBalance,
  Receipt,
  People,
  ShoppingCart,
  Assessment,
  Settings,
  ExpandLess,
  ExpandMore,
  Book,
  Description,
  Payment,
  LocalShipping,
  Business,
  Assignment,
  Gavel,
  TrendingUp,
  Analytics,
} from '@mui/icons-material';

interface MenuItem {
  id: string;
  label: string;
  icon: React.ReactNode;
  path?: string;
  children?: MenuItem[];
}

const menuItems: MenuItem[] = [
  {
    id: 'dashboard',
    label: 'Dashboard',
    icon: <Dashboard />,
    path: '/dashboard',
  },
  {
    id: 'general-ledger',
    label: 'General Ledger',
    icon: <AccountBalance />,
    children: [
      {
        id: 'chart-of-accounts',
        label: 'Chart of Accounts',
        icon: <Book />,
        path: '/general-ledger/chart-of-accounts',
      },
      {
        id: 'journal-entries',
        label: 'Journal Entries',
        icon: <Description />,
        path: '/general-ledger/journal-entries',
      },
      {
        id: 'financial-statements',
        label: 'Financial Statements',
        icon: <Assessment />,
        path: '/general-ledger/financial-statements',
      },
    ],
  },
  {
    id: 'accounts-payable',
    label: 'Accounts Payable',
    icon: <Receipt />,
    children: [
      {
        id: 'vendors',
        label: 'Vendors',
        icon: <Business />,
        path: '/accounts-payable/vendors',
      },
      {
        id: 'invoices',
        label: 'Invoices',
        icon: <Description />,
        path: '/accounts-payable/invoices',
      },
      {
        id: 'payments',
        label: 'Payments',
        icon: <Payment />,
        path: '/accounts-payable/payments',
      },
      {
        id: 'purchase-orders',
        label: 'Purchase Orders',
        icon: <Assignment />,
        path: '/accounts-payable/purchase-orders',
      },
    ],
  },
  {
    id: 'accounts-receivable',
    label: 'Accounts Receivable',
    icon: <People />,
    children: [
      {
        id: 'customers',
        label: 'Customers',
        icon: <People />,
        path: '/accounts-receivable/customers',
      },
      {
        id: 'invoices',
        label: 'Invoices',
        icon: <Description />,
        path: '/accounts-receivable/invoices',
      },
      {
        id: 'collections',
        label: 'Collections',
        icon: <Payment />,
        path: '/accounts-receivable/collections',
      },
      {
        id: 'sales-orders',
        label: 'Sales Orders',
        icon: <LocalShipping />,
        path: '/accounts-receivable/sales-orders',
      },
    ],
  },
  {
    id: 'procurement',
    label: 'Procurement',
    icon: <ShoppingCart />,
    children: [
      {
        id: 'suppliers',
        label: 'Suppliers',
        icon: <Business />,
        path: '/procurement/suppliers',
      },
      {
        id: 'purchase-requisitions',
        label: 'Purchase Requisitions',
        icon: <Assignment />,
        path: '/procurement/purchase-requisitions',
      },
      {
        id: 'rfqs',
        label: 'RFQs',
        icon: <Gavel />,
        path: '/procurement/rfqs',
      },
      {
        id: 'contracts',
        label: 'Contracts',
        icon: <Description />,
        path: '/procurement/contracts',
      },
    ],
  },
  {
    id: 'reports',
    label: 'Reports & Analytics',
    icon: <Assessment />,
    children: [
      {
        id: 'reports',
        label: 'Reports',
        icon: <Assessment />,
        path: '/reports',
      },
      {
        id: 'analytics',
        label: 'Analytics',
        icon: <Analytics />,
        path: '/reports/analytics',
      },
      {
        id: 'trends',
        label: 'Trends',
        icon: <TrendingUp />,
        path: '/reports/trends',
      },
    ],
  },
  {
    id: 'settings',
    label: 'Settings',
    icon: <Settings />,
    children: [
      {
        id: 'general',
        label: 'General',
        icon: <Settings />,
        path: '/settings',
      },
      {
        id: 'users',
        label: 'User Management',
        icon: <People />,
        path: '/settings/users',
      },
    ],
  },
];

const Sidebar: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [expandedItems, setExpandedItems] = useState<string[]>(['dashboard']);

  const handleItemClick = (item: MenuItem) => {
    if (item.path) {
      navigate(item.path);
    } else if (item.children) {
      setExpandedItems((prev) =>
        prev.includes(item.id)
          ? prev.filter((id) => id !== item.id)
          : [...prev, item.id]
      );
    }
  };

  const isItemActive = (item: MenuItem): boolean => {
    if (item.path) {
      return location.pathname === item.path;
    }
    if (item.children) {
      return item.children.some((child) => isItemActive(child));
    }
    return false;
  };

  const isItemExpanded = (itemId: string): boolean => {
    return expandedItems.includes(itemId);
  };

  const renderMenuItem = (item: MenuItem, level: number = 0) => {
    const isActive = isItemActive(item);
    const isExpanded = isItemExpanded(item.id);
    const hasChildren = item.children && item.children.length > 0;

    return (
      <Box key={item.id}>
        <ListItem disablePadding>
          <ListItemButton
            onClick={() => handleItemClick(item)}
            selected={isActive}
            sx={{
              pl: 2 + level * 2,
              '&.Mui-selected': {
                backgroundColor: 'primary.light',
                color: 'primary.contrastText',
                '&:hover': {
                  backgroundColor: 'primary.main',
                },
              },
            }}
          >
            <ListItemIcon
              sx={{
                color: isActive ? 'primary.contrastText' : 'inherit',
                minWidth: 40,
              }}
            >
              {item.icon}
            </ListItemIcon>
            <ListItemText
              primary={
                <Typography variant="body2" sx={{ fontWeight: isActive ? 600 : 400 }}>
                  {item.label}
                </Typography>
              }
            />
            {hasChildren && (isExpanded ? <ExpandLess /> : <ExpandMore />)}
          </ListItemButton>
        </ListItem>
        
        {hasChildren && (
          <Collapse in={isExpanded} timeout="auto" unmountOnExit>
            <List component="div" disablePadding>
              {item.children!.map((child) => renderMenuItem(child, level + 1))}
            </List>
          </Collapse>
        )}
      </Box>
    );
  };

  return (
    <Box sx={{ overflow: 'auto' }}>
      <List>
        {menuItems.map((item) => renderMenuItem(item))}
      </List>
    </Box>
  );
};

export default Sidebar; 