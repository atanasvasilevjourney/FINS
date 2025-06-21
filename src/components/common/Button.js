import React from 'react';
import {
  TouchableOpacity,
  Text,
  StyleSheet,
  ActivityIndicator,
} from 'react-native';
import { useTheme } from '../../context/ThemeContext';

const Button = ({
  title,
  onPress,
  variant = 'primary',
  size = 'medium',
  disabled = false,
  loading = false,
  icon,
  style,
  textStyle,
  ...props
}) => {
  const theme = useTheme();
  
  const getButtonStyle = () => {
    const baseStyle = {
      flexDirection: 'row',
      alignItems: 'center',
      justifyContent: 'center',
      borderRadius: theme.borderRadius.medium,
      ...theme.shadows.small,
    };
    
    const sizeStyles = {
      small: {
        paddingVertical: theme.spacing.sm,
        paddingHorizontal: theme.spacing.md,
        minHeight: 40,
      },
      medium: {
        paddingVertical: theme.spacing.md,
        paddingHorizontal: theme.spacing.lg,
        minHeight: 48,
      },
      large: {
        paddingVertical: theme.spacing.lg,
        paddingHorizontal: theme.spacing.xl,
        minHeight: 56,
      },
    };
    
    const variantStyles = {
      primary: {
        backgroundColor: theme.colors.primary,
      },
      secondary: {
        backgroundColor: 'transparent',
        borderWidth: 2,
        borderColor: theme.colors.primary,
      },
      success: {
        backgroundColor: theme.colors.success,
      },
      error: {
        backgroundColor: theme.colors.error,
      },
      warning: {
        backgroundColor: theme.colors.warning,
      },
      ghost: {
        backgroundColor: 'transparent',
      },
    };
    
    const disabledStyle = disabled ? {
      backgroundColor: theme.colors.textLight,
      borderColor: theme.colors.textLight,
    } : {};
    
    return [
      baseStyle,
      sizeStyles[size],
      variantStyles[variant],
      disabledStyle,
      style,
    ];
  };
  
  const getTextStyle = () => {
    const baseTextStyle = {
      fontFamily: theme.typography.fontFamilyBold,
      textAlign: 'center',
      letterSpacing: theme.typography.letterSpacing.small,
    };
    
    const sizeTextStyles = {
      small: {
        fontSize: theme.typography.fontSize.small,
      },
      medium: {
        fontSize: theme.typography.fontSize.medium,
      },
      large: {
        fontSize: theme.typography.fontSize.large,
      },
    };
    
    const variantTextStyles = {
      primary: {
        color: theme.colors.textInverse,
      },
      secondary: {
        color: theme.colors.primary,
      },
      success: {
        color: theme.colors.textInverse,
      },
      error: {
        color: theme.colors.textInverse,
      },
      warning: {
        color: theme.colors.textInverse,
      },
      ghost: {
        color: theme.colors.text,
      },
    };
    
    const disabledTextStyle = disabled ? {
      color: theme.colors.textSecondary,
    } : {};
    
    return [
      baseTextStyle,
      sizeTextStyles[size],
      variantTextStyles[variant],
      disabledTextStyle,
      textStyle,
    ];
  };
  
  return (
    <TouchableOpacity
      style={getButtonStyle()}
      onPress={onPress}
      disabled={disabled || loading}
      activeOpacity={0.8}
      accessibilityRole="button"
      accessibilityLabel={title}
      accessibilityState={{ disabled: disabled || loading }}
      {...props}
    >
      {loading ? (
        <ActivityIndicator
          size="small"
          color={variant === 'secondary' ? theme.colors.primary : theme.colors.textInverse}
        />
      ) : (
        <>
          {icon && icon}
          <Text style={getTextStyle()}>{title}</Text>
        </>
      )}
    </TouchableOpacity>
  );
};

export default Button; 