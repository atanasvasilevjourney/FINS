import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
} from 'react-native';
import { useTheme } from '../context/ThemeContext';
import Icon from 'react-native-vector-icons/MaterialIcons';

const TutorialScreen = () => {
  const theme = useTheme();
  
  const tutorialSteps = [
    {
      title: 'Как да играете',
      description: 'Кръстословица+ е игра, в която трябва да намерите думи в мрежа от букви.',
      icon: 'extension',
    },
    {
      title: 'Избор на букви',
      description: 'Докоснете буквите в мрежата, за да ги изберете и да съставите дума.',
      icon: 'touch-app',
    },
    {
      title: 'Подсказки',
      description: 'Използвайте подсказките отдясно, за да разберете какви думи трябва да намерите.',
      icon: 'lightbulb',
    },
    {
      title: 'Потвърждение',
      description: 'След като изберете буквите, натиснете "Потвърди" за да проверите думата.',
      icon: 'check-circle',
    },
    {
      title: 'Точки',
      description: 'Получавате точки за всяка правилна дума. Колкото по-бързо решите, толкова повече точки.',
      icon: 'stars',
    },
  ];
  
  const styles = StyleSheet.create({
    container: {
      flex: 1,
      backgroundColor: theme.colors.background,
    },
    content: {
      padding: theme.spacing.lg,
    },
    header: {
      alignItems: 'center',
      marginBottom: theme.spacing.xl,
    },
    title: {
      fontSize: theme.typography.fontSize.title,
      fontFamily: theme.typography.fontFamilyBold,
      color: theme.colors.text,
      textAlign: 'center',
      marginBottom: theme.spacing.sm,
    },
    subtitle: {
      fontSize: theme.typography.fontSize.medium,
      fontFamily: theme.typography.fontFamily,
      color: theme.colors.textSecondary,
      textAlign: 'center',
    },
    stepContainer: {
      backgroundColor: theme.colors.backgroundCard,
      padding: theme.spacing.lg,
      borderRadius: theme.borderRadius.large,
      marginBottom: theme.spacing.lg,
      ...theme.shadows.medium,
    },
    stepHeader: {
      flexDirection: 'row',
      alignItems: 'center',
      marginBottom: theme.spacing.md,
    },
    stepIcon: {
      width: 50,
      height: 50,
      borderRadius: theme.borderRadius.round,
      backgroundColor: theme.colors.primaryLight,
      justifyContent: 'center',
      alignItems: 'center',
      marginRight: theme.spacing.md,
    },
    stepTitle: {
      fontSize: theme.typography.fontSize.large,
      fontFamily: theme.typography.fontFamilyBold,
      color: theme.colors.text,
      flex: 1,
    },
    stepDescription: {
      fontSize: theme.typography.fontSize.medium,
      fontFamily: theme.typography.fontFamily,
      color: theme.colors.text,
      lineHeight: theme.typography.lineHeight.medium * theme.typography.fontSize.medium,
    },
    tipsContainer: {
      backgroundColor: theme.colors.backgroundCard,
      padding: theme.spacing.lg,
      borderRadius: theme.borderRadius.large,
      marginBottom: theme.spacing.lg,
      ...theme.shadows.medium,
    },
    tipsTitle: {
      fontSize: theme.typography.fontSize.large,
      fontFamily: theme.typography.fontFamilyBold,
      color: theme.colors.text,
      marginBottom: theme.spacing.md,
    },
    tipItem: {
      flexDirection: 'row',
      alignItems: 'flex-start',
      marginBottom: theme.spacing.sm,
    },
    tipIcon: {
      marginRight: theme.spacing.sm,
      marginTop: 2,
    },
    tipText: {
      flex: 1,
      fontSize: theme.typography.fontSize.medium,
      fontFamily: theme.typography.fontFamily,
      color: theme.colors.text,
    },
    startButton: {
      backgroundColor: theme.colors.primary,
      paddingVertical: theme.spacing.lg,
      paddingHorizontal: theme.spacing.xl,
      borderRadius: theme.borderRadius.large,
      alignItems: 'center',
      marginTop: theme.spacing.lg,
      ...theme.shadows.medium,
    },
    startButtonText: {
      fontSize: theme.typography.fontSize.large,
      fontFamily: theme.typography.fontFamilyBold,
      color: theme.colors.textInverse,
      textTransform: 'uppercase',
      letterSpacing: theme.typography.letterSpacing.medium,
    },
  });
  
  const tips = [
    'Започнете с по-късите думи',
    'Използвайте подсказките, ако се затрудните',
    'Планирайте времето си добре',
    'Практикувайте редовно за по-добри резултати',
  ];
  
  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <View style={styles.header}>
        <Text style={styles.title}>Как да играете</Text>
        <Text style={styles.subtitle}>
          Научете основите на играта и започнете да се забавлявате!
        </Text>
      </View>
      
      {tutorialSteps.map((step, index) => (
        <View key={index} style={styles.stepContainer}>
          <View style={styles.stepHeader}>
            <View style={styles.stepIcon}>
              <Icon name={step.icon} size={24} color={theme.colors.primary} />
            </View>
            <Text style={styles.stepTitle}>{step.title}</Text>
          </View>
          <Text style={styles.stepDescription}>{step.description}</Text>
        </View>
      ))}
      
      <View style={styles.tipsContainer}>
        <Text style={styles.tipsTitle}>Полезни съвети</Text>
        {tips.map((tip, index) => (
          <View key={index} style={styles.tipItem}>
            <Icon
              name="check"
              size={20}
              color={theme.colors.success}
              style={styles.tipIcon}
            />
            <Text style={styles.tipText}>{tip}</Text>
          </View>
        ))}
      </View>
      
      <TouchableOpacity style={styles.startButton} activeOpacity={0.8}>
        <Text style={styles.startButtonText}>Започнете играта</Text>
      </TouchableOpacity>
    </ScrollView>
  );
};

export default TutorialScreen; 