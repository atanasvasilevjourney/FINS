import React, { useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  Image,
  SafeAreaView,
} from 'react-native';
import { useDispatch } from 'react-redux';
import { useNavigation } from '@react-navigation/native';
import { useTheme } from '../context/ThemeContext';
import { setUser } from '../store/userSlice';
import Icon from 'react-native-vector-icons/MaterialIcons';

const WelcomeScreen = () => {
  const navigation = useNavigation();
  const dispatch = useDispatch();
  const theme = useTheme();
  
  const handleStartGame = () => {
    // Create a simple user profile for demo
    dispatch(setUser({
      id: 'demo_user_001',
      username: 'Играч',
      email: 'demo@example.com'
    }));
  };
  
  const handleTutorial = () => {
    navigation.navigate('Tutorial');
  };
  
  const styles = StyleSheet.create({
    container: {
      flex: 1,
      backgroundColor: theme.colors.background,
    },
    content: {
      flex: 1,
      padding: theme.spacing.lg,
      justifyContent: 'center',
    },
    header: {
      alignItems: 'center',
      marginBottom: theme.spacing.xxl,
    },
    title: {
      fontSize: theme.typography.fontSize.title,
      fontFamily: theme.typography.fontFamilyBold,
      color: theme.colors.text,
      textAlign: 'center',
      marginBottom: theme.spacing.sm,
    },
    subtitle: {
      fontSize: theme.typography.fontSize.large,
      fontFamily: theme.typography.fontFamily,
      color: theme.colors.textSecondary,
      textAlign: 'center',
      marginBottom: theme.spacing.xl,
    },
    logo: {
      width: 120,
      height: 120,
      marginBottom: theme.spacing.lg,
      borderRadius: theme.borderRadius.large,
      backgroundColor: theme.colors.primary,
      justifyContent: 'center',
      alignItems: 'center',
    },
    logoText: {
      fontSize: 48,
      fontFamily: theme.typography.fontFamilyBold,
      color: theme.colors.textInverse,
    },
    features: {
      marginBottom: theme.spacing.xxl,
    },
    featureItem: {
      flexDirection: 'row',
      alignItems: 'center',
      padding: theme.spacing.md,
      marginBottom: theme.spacing.md,
      backgroundColor: theme.colors.backgroundCard,
      borderRadius: theme.borderRadius.medium,
      ...theme.shadows.small,
    },
    featureIcon: {
      width: 50,
      height: 50,
      borderRadius: theme.borderRadius.round,
      backgroundColor: theme.colors.primaryLight,
      justifyContent: 'center',
      alignItems: 'center',
      marginRight: theme.spacing.md,
    },
    featureText: {
      flex: 1,
      fontSize: theme.typography.fontSize.medium,
      fontFamily: theme.typography.fontFamily,
      color: theme.colors.text,
    },
    actions: {
      gap: theme.spacing.md,
    },
    primaryButton: {
      backgroundColor: theme.colors.primary,
      paddingVertical: theme.spacing.lg,
      paddingHorizontal: theme.spacing.xl,
      borderRadius: theme.borderRadius.large,
      alignItems: 'center',
      ...theme.shadows.medium,
    },
    primaryButtonText: {
      fontSize: theme.typography.fontSize.large,
      fontFamily: theme.typography.fontFamilyBold,
      color: theme.colors.textInverse,
      textTransform: 'uppercase',
      letterSpacing: theme.typography.letterSpacing.medium,
    },
    secondaryButton: {
      backgroundColor: 'transparent',
      paddingVertical: theme.spacing.lg,
      paddingHorizontal: theme.spacing.xl,
      borderRadius: theme.borderRadius.large,
      alignItems: 'center',
      borderWidth: 2,
      borderColor: theme.colors.primary,
    },
    secondaryButtonText: {
      fontSize: theme.typography.fontSize.medium,
      fontFamily: theme.typography.fontFamilyBold,
      color: theme.colors.primary,
    },
    footer: {
      padding: theme.spacing.lg,
      alignItems: 'center',
    },
    footerText: {
      fontSize: theme.typography.fontSize.small,
      fontFamily: theme.typography.fontFamily,
      color: theme.colors.textLight,
      textAlign: 'center',
    },
  });
  
  const features = [
    {
      icon: '🧠',
      text: 'Тренировка на паметта и логическото мислене',
    },
    {
      icon: '📚',
      text: 'Богат български речник с над 1000 думи',
    },
    {
      icon: '🎯',
      text: 'Дневни предизвикателства и теми',
    },
    {
      icon: '👥',
      text: 'Класации и постижения',
    },
    {
      icon: '♿',
      text: 'Достъпност за всички възрасти',
    },
  ];
  
  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.content} showsVerticalScrollIndicator={false}>
        <View style={styles.header}>
          <View style={styles.logo}>
            <Text style={styles.logoText}>К+</Text>
          </View>
          <Text style={styles.title}>Кръстословица+</Text>
          <Text style={styles.subtitle}>Упражнете ума си с български думи</Text>
        </View>
        
        <View style={styles.features}>
          {features.map((feature, index) => (
            <View key={index} style={styles.featureItem}>
              <View style={styles.featureIcon}>
                <Text style={{ fontSize: 24 }}>{feature.icon}</Text>
              </View>
              <Text style={styles.featureText}>{feature.text}</Text>
            </View>
          ))}
        </View>
        
        <View style={styles.actions}>
          <TouchableOpacity
            style={styles.primaryButton}
            onPress={handleStartGame}
            activeOpacity={0.8}
          >
            <Text style={styles.primaryButtonText}>Започнете сега</Text>
          </TouchableOpacity>
          
          <TouchableOpacity
            style={styles.secondaryButton}
            onPress={handleTutorial}
            activeOpacity={0.8}
          >
            <Text style={styles.secondaryButtonText}>Как да играете</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
      
      <View style={styles.footer}>
        <Text style={styles.footerText}>
          Създадено с ❤️ за българските играчи
        </Text>
        <Text style={styles.footerText}>
          Версия 1.0.0
        </Text>
      </View>
    </SafeAreaView>
  );
};

export default WelcomeScreen; 