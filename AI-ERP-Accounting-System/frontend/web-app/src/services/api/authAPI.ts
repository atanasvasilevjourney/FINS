import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:80';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to include auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor to handle auth errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface LoginResponse {
  token: string;
  user: {
    id: number;
    username: string;
    email: string;
    firstName: string;
    lastName: string;
    role: string;
    permissions: string[];
    entityId?: number;
    entityName?: string;
  };
}

export const authAPI = {
  // Login user
  login: async (credentials: LoginCredentials): Promise<LoginResponse> => {
    try {
      // For demo purposes, simulate API call
      if (credentials.username === 'admin' && credentials.password === 'admin123') {
        const mockResponse: LoginResponse = {
          token: 'mock-jwt-token-' + Date.now(),
          user: {
            id: 1,
            username: 'admin',
            email: 'admin@finserp.com',
            firstName: 'Admin',
            lastName: 'User',
            role: 'admin',
            permissions: ['read', 'write', 'delete', 'admin'],
            entityId: 1,
            entityName: 'FINS ERP',
          },
        };
        
        // Simulate network delay
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        return mockResponse;
      } else {
        throw new Error('Invalid credentials');
      }
    } catch (error) {
      throw error;
    }
  },

  // Logout user
  logout: async (): Promise<void> => {
    try {
      // In a real app, you would call the logout endpoint
      // await apiClient.post('/auth/logout');
      
      // For demo purposes, just simulate a delay
      await new Promise(resolve => setTimeout(resolve, 500));
    } catch (error) {
      throw error;
    }
  },

  // Get current user
  getCurrentUser: async (): Promise<LoginResponse['user']> => {
    try {
      // For demo purposes, simulate API call
      const mockUser: LoginResponse['user'] = {
        id: 1,
        username: 'admin',
        email: 'admin@finserp.com',
        firstName: 'Admin',
        lastName: 'User',
        role: 'admin',
        permissions: ['read', 'write', 'delete', 'admin'],
        entityId: 1,
        entityName: 'FINS ERP',
      };
      
      // Simulate network delay
      await new Promise(resolve => setTimeout(resolve, 500));
      
      return mockUser;
    } catch (error) {
      throw error;
    }
  },

  // Refresh token
  refreshToken: async (): Promise<{ token: string }> => {
    try {
      const response = await apiClient.post('/auth/refresh');
      return response.data;
    } catch (error) {
      throw error;
    }
  },
};

export default authAPI; 