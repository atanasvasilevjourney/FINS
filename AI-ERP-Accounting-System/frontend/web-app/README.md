# FINS ERP - React Frontend Application

A modern, responsive React-based web application for the FINS ERP Accounting System. Built with TypeScript, Material-UI, and Redux Toolkit for optimal performance and developer experience.

## 🚀 Features

### Core Functionality
- **Authentication & Authorization**: Secure login system with role-based access control
- **Responsive Design**: Mobile-first approach with Material-UI components
- **Real-time Updates**: React Query for efficient data fetching and caching
- **State Management**: Redux Toolkit for predictable state management
- **Type Safety**: Full TypeScript support for better development experience

### ERP Modules
- **Dashboard**: Financial overview with charts and key metrics
- **General Ledger**: Chart of accounts, journal entries, financial statements
- **Accounts Payable**: Vendor management, invoice processing, payments
- **Accounts Receivable**: Customer management, invoice generation, collections
- **Procurement**: Supplier management, purchase requisitions, RFQs, contracts
- **Reports & Analytics**: Comprehensive reporting and data visualization
- **Settings**: User management and system configuration

## 🛠️ Technology Stack

- **React 18** - Modern React with hooks and concurrent features
- **TypeScript** - Type-safe JavaScript development
- **Material-UI (MUI)** - Professional UI component library
- **Redux Toolkit** - Simplified Redux for state management
- **React Query** - Data fetching and caching
- **React Router** - Client-side routing
- **Recharts** - Data visualization library
- **Axios** - HTTP client for API communication
- **Formik & Yup** - Form handling and validation

## 📦 Installation

1. **Navigate to the frontend directory**:
   ```bash
   cd AI-ERP-Accounting-System/frontend/web-app
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm start
   ```

4. **Open your browser** and navigate to `http://localhost:3000`

## 🔧 Available Scripts

- `npm start` - Start development server
- `npm build` - Build for production
- `npm test` - Run tests
- `npm run lint` - Run ESLint
- `npm run lint:fix` - Fix ESLint errors
- `npm run format` - Format code with Prettier
- `npm run type-check` - Run TypeScript type checking

## 🏗️ Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── Auth/           # Authentication components
│   ├── Layout/         # Layout and navigation
│   └── common/         # Common UI components
├── pages/              # Page components
│   ├── Auth/           # Authentication pages
│   ├── Dashboard/      # Dashboard pages
│   ├── GeneralLedger/  # GL module pages
│   ├── AccountsPayable/# AP module pages
│   ├── AccountsReceivable/ # AR module pages
│   ├── Procurement/    # Procurement pages
│   ├── Reports/        # Reports and analytics
│   └── Settings/       # Settings pages
├── store/              # Redux store configuration
│   ├── slices/         # Redux slices
│   └── store.ts        # Store configuration
├── services/           # API services
│   └── api/            # API client and endpoints
├── utils/              # Utility functions
├── types/              # TypeScript type definitions
├── hooks/              # Custom React hooks
└── styles/             # Global styles and themes
```

## 🎨 UI/UX Features

### Design System
- **Material Design**: Following Google's Material Design principles
- **Responsive Grid**: Adaptive layout for all screen sizes
- **Dark/Light Theme**: Theme switching capability
- **Accessibility**: WCAG 2.1 compliant components

### Components
- **Data Grids**: Advanced data tables with sorting, filtering, and pagination
- **Charts**: Interactive charts for financial data visualization
- **Forms**: Comprehensive form components with validation
- **Modals**: Dialog components for data entry and confirmation
- **Notifications**: Toast notifications for user feedback

## 🔐 Authentication

The application uses JWT-based authentication with the following features:

- **Login/Logout**: Secure authentication flow
- **Token Management**: Automatic token refresh and storage
- **Route Protection**: Protected routes for authenticated users
- **Role-based Access**: Different permissions based on user roles

### Demo Credentials
- **Username**: `admin`
- **Password**: `admin123`

## 📊 State Management

### Redux Store Structure
- **Auth Slice**: User authentication and session management
- **UI Slice**: UI state (sidebar, notifications, theme)
- **General Ledger Slice**: Chart of accounts and journal entries
- **Accounts Payable Slice**: Vendors, invoices, and payments
- **Accounts Receivable Slice**: Customers, invoices, and collections
- **Procurement Slice**: Suppliers, requisitions, RFQs, and contracts

### Data Flow
1. **API Calls**: React Query handles data fetching and caching
2. **State Updates**: Redux Toolkit manages application state
3. **UI Updates**: React components re-render based on state changes

## 🌐 API Integration

The frontend communicates with the backend through RESTful APIs:

- **Base URL**: `http://localhost:80` (configurable via environment variables)
- **Authentication**: Bearer token in Authorization header
- **Error Handling**: Centralized error handling with user-friendly messages
- **Request/Response Interceptors**: Automatic token management and error handling

## 📱 Responsive Design

The application is fully responsive and optimized for:

- **Desktop**: Full-featured interface with sidebar navigation
- **Tablet**: Adaptive layout with collapsible sidebar
- **Mobile**: Mobile-first design with touch-friendly interactions

## 🧪 Testing

### Testing Strategy
- **Unit Tests**: Component testing with React Testing Library
- **Integration Tests**: API integration testing
- **E2E Tests**: End-to-end testing with Cypress (planned)

### Running Tests
```bash
npm test
```

## 🚀 Deployment

### Production Build
```bash
npm run build
```

### Environment Variables
Create a `.env` file in the root directory:

```env
REACT_APP_API_URL=http://localhost:80
REACT_APP_ENVIRONMENT=production
```

### Docker Deployment
```bash
# Build Docker image
docker build -t fins-erp-frontend .

# Run container
docker run -p 3000:3000 fins-erp-frontend
```

## 🔧 Development Guidelines

### Code Style
- **ESLint**: Enforced code style and best practices
- **Prettier**: Automatic code formatting
- **TypeScript**: Strict type checking enabled

### Component Guidelines
- **Functional Components**: Use functional components with hooks
- **Props Interface**: Define TypeScript interfaces for all props
- **Error Boundaries**: Implement error boundaries for robust error handling
- **Loading States**: Provide loading indicators for async operations

### State Management Best Practices
- **Normalized State**: Use normalized state structure for complex data
- **Selectors**: Use selectors for derived state
- **Async Actions**: Use Redux Toolkit's createAsyncThunk for async operations

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- **Documentation**: Check the project documentation
- **Issues**: Create an issue in the repository
- **Email**: Contact the development team

## 🔄 Version History

- **v2.0.0** - Complete React frontend with all ERP modules
- **v1.0.0** - Initial Streamlit-based application

---

**FINS ERP** - Empowering businesses with intelligent financial management. 