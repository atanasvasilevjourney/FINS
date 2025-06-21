import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ActivityIndicator,
} from 'react-native';
import { useTheme } from '../../context/ThemeContext';

const SplashScreen = () => {
  const theme = useTheme();
  
  const styles = StyleSheet.create({
    container: {
      flex: 1,
      justifyContent: 'center',
      alignItems: 'center',
      backgroundColor: theme.colors.background,
    },
    logo: {
      width: 120,
      height: 120,
      borderRadius: theme.borderRadius.large,
      backgroundColor: theme.colors.primary,
      justifyContent: 'center',
      alignItems: 'center',
      marginBottom: theme.spacing.xl,
      ...theme.shadows.large,
    },
    logoText: {
      fontSize: 48,
      fontFamily: theme.typography.fontFamilyBold,
      color: theme.colors.textInverse,
    },
    title: {
      fontSize: theme.typography.fontSize.title,
      fontFamily: theme.typography.fontFamilyBold,
      color: theme.colors.text,
      marginBottom: theme.spacing.sm,
    },
    subtitle: {
      fontSize: theme.typography.fontSize.medium,
      fontFamily: theme.typography.fontFamily,
      color: theme.colors.textSecondary,
      marginBottom: theme.spacing.xxl,
    },
    loadingContainer: {
      alignItems: 'center',
    },
    loadingText: {
      fontSize: theme.typography.fontSize.medium,
      fontFamily: theme.typography.fontFamily,
      color: theme.colors.textSecondary,
      marginTop: theme.spacing.md,
    },
  });
  
  return (
    <View style={styles.container}>
      <View style={styles.logo}>
        <Text style={styles.logoText}>К+</Text>
      </View>
      
      <Text style={styles.title}>Кръстословица+</Text>
      <Text style={styles.subtitle}>Упражнете ума си</Text>
      
      <View style={styles.loadingContainer}>
        <ActivityIndicator
          size="large"
          color={theme.colors.primary}
        />
        <Text style={styles.loadingText}>Зареждане...</Text>
      </View>
    </View>
  );
};

export default SplashScreen; 