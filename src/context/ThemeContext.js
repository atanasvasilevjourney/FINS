import React, { createContext, useContext, useState, useEffect } from 'react';
import { useColorScheme } from 'react-native';
import { useSelector } from 'react-redux';

const ThemeContext = createContext();

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};

export const ThemeProvider = ({ children }) => {
  const systemColorScheme = useColorScheme();
  const settings = useSelector(state => state.settings);
  
  const [currentTheme, setCurrentTheme] = useState('light');
  
  useEffect(() => {
    if (settings.theme === 'auto') {
      setCurrentTheme(systemColorScheme || 'light');
    } else {
      setCurrentTheme(settings.theme);
    }
  }, [settings.theme, systemColorScheme]);
  
  const theme = {
    // Colors
    colors: {
      // Primary Colors
      primary: currentTheme === 'dark' ? '#7BB3F0' : '#4A90E2',
      primaryDark: currentTheme === 'dark' ? '#5A9BE0' : '#357ABD',
      primaryLight: currentTheme === 'dark' ? '#9BC7F5' : '#7BB3F0',
      
      // Secondary Colors
      secondary: currentTheme === 'dark' ? '#9ADE4A' : '#7ED321',
      secondaryDark: currentTheme === 'dark' ? '#8AD43A' : '#6BB61A',
      secondaryLight: currentTheme === 'dark' ? '#B0E66A' : '#9ADE4A',
      
      // Accent Colors
      accent: currentTheme === 'dark' ? '#F7B849' : '#F5A623',
      accentDark: currentTheme === 'dark' ? '#F5A623' : '#E8931C',
      accentLight: currentTheme === 'dark' ? '#F9C869' : '#F7B849',
      
      // Background Colors
      background: currentTheme === 'dark' ? '#1A1A1A' : '#FAFAFA',
      backgroundSecondary: currentTheme === 'dark' ? '#2D2D2D' : '#F5F5F5',
      backgroundCard: currentTheme === 'dark' ? '#3A3A3A' : '#FFFFFF',
      backgroundOverlay: currentTheme === 'dark' ? 'rgba(0,0,0,0.7)' : 'rgba(0,0,0,0.5)',
      
      // Text Colors
      text: currentTheme === 'dark' ? '#E0E0E0' : '#2C3E50',
      textSecondary: currentTheme === 'dark' ? '#B0B0B0' : '#7F8C8D',
      textLight: currentTheme === 'dark' ? '#808080' : '#BDC3C7',
      textInverse: currentTheme === 'dark' ? '#2C3E50' : '#FFFFFF',
      
      // Status Colors
      success: currentTheme === 'dark' ? '#4CAF50' : '#27AE60',
      error: currentTheme === 'dark' ? '#F44336' : '#E74C3C',
      warning: currentTheme === 'dark' ? '#FF9800' : '#F39C12',
      info: currentTheme === 'dark' ? '#2196F3' : '#3498DB',
      
      // Border Colors
      border: currentTheme === 'dark' ? '#4A4A4A' : '#E0E0E0',
      borderLight: currentTheme === 'dark' ? '#3A3A3A' : '#F0F0F0',
      
      // Shadow Colors
      shadow: currentTheme === 'dark' ? 'rgba(0,0,0,0.8)' : 'rgba(0,0,0,0.1)',
      
      // High Contrast Mode
      ...(settings.highContrast && {
        text: currentTheme === 'dark' ? '#FFFFFF' : '#000000',
        background: currentTheme === 'dark' ? '#000000' : '#FFFFFF',
        border: currentTheme === 'dark' ? '#FFFFFF' : '#000000',
      })
    },
    
    // Typography
    typography: {
      fontFamily: 'Roboto',
      fontFamilyBold: 'Roboto-Bold',
      fontFamilyMedium: 'Roboto-Medium',
      
      // Font sizes based on user preference
      fontSize: {
        small: settings.fontSize === 'small' ? 16 : 
               settings.fontSize === 'medium' ? 18 :
               settings.fontSize === 'large' ? 20 : 22,
        medium: settings.fontSize === 'small' ? 18 :
                settings.fontSize === 'medium' ? 20 :
                settings.fontSize === 'large' ? 22 : 24,
        large: settings.fontSize === 'small' ? 20 :
               settings.fontSize === 'medium' ? 22 :
               settings.fontSize === 'large' ? 24 : 26,
        xlarge: settings.fontSize === 'small' ? 24 :
                settings.fontSize === 'medium' ? 26 :
                settings.fontSize === 'large' ? 28 : 30,
        title: settings.fontSize === 'small' ? 28 :
               settings.fontSize === 'medium' ? 30 :
               settings.fontSize === 'large' ? 32 : 34,
      },
      
      lineHeight: {
        small: 1.3,
        medium: 1.4,
        large: 1.5,
        xlarge: 1.6,
      },
      
      letterSpacing: {
        small: 0.2,
        medium: 0.5,
        large: 0.8,
      }
    },
    
    // Spacing
    spacing: {
      xs: 4,
      sm: 8,
      md: 16,
      lg: 24,
      xl: 32,
      xxl: 48,
    },
    
    // Border Radius
    borderRadius: {
      small: 4,
      medium: 8,
      large: 12,
      xlarge: 16,
      round: 50,
    },
    
    // Shadows
    shadows: {
      small: {
        shadowColor: currentTheme === 'dark' ? '#000000' : '#000000',
        shadowOffset: { width: 0, height: 1 },
        shadowOpacity: currentTheme === 'dark' ? 0.8 : 0.1,
        shadowRadius: 2,
        elevation: 2,
      },
      medium: {
        shadowColor: currentTheme === 'dark' ? '#000000' : '#000000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: currentTheme === 'dark' ? 0.8 : 0.15,
        shadowRadius: 4,
        elevation: 4,
      },
      large: {
        shadowColor: currentTheme === 'dark' ? '#000000' : '#000000',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: currentTheme === 'dark' ? 0.8 : 0.2,
        shadowRadius: 8,
        elevation: 8,
      },
    },
    
    // Animation
    animation: {
      duration: settings.reduceMotion ? 0 : 300,
      easing: 'ease-out',
    },
    
    // Current theme info
    isDark: currentTheme === 'dark',
    isLight: currentTheme === 'light',
  };
  
  return (
    <ThemeContext.Provider value={theme}>
      {children}
    </ThemeContext.Provider>
  );
}; 