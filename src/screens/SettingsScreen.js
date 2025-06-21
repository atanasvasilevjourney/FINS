import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  Switch,
  TouchableOpacity,
  Alert,
} from 'react-native';
import { useSelector, useDispatch } from 'react-redux';
import { useTheme } from '../context/ThemeContext';
import {
  setFontSize,
  toggleHighContrast,
  toggleReduceMotion,
  toggleSound,
  toggleHapticFeedback,
  setTheme,
  setDifficulty,
  resetToDefaults,
} from '../store/settingsSlice';
import Button from '../components/common/Button';
import Icon from 'react-native-vector-icons/MaterialIcons';

const SettingsScreen = () => {
  const dispatch = useDispatch();
  const theme = useTheme();
  const settings = useSelector(state => state.settings);
  
  const handleResetSettings = () => {
    Alert.alert(
      'Нулиране на настройките',
      'Сигурни ли сте, че искате да нулирате всички настройки?',
      [
        { text: 'Отказ', style: 'cancel' },
        { 
          text: 'Нулирай', 
          style: 'destructive',
          onPress: () => dispatch(resetToDefaults())
        }
      ]
    );
  };
  
  const styles = StyleSheet.create({
    container: {
      flex: 1,
      backgroundColor: theme.colors.background,
    },
    content: {
      padding: theme.spacing.md,
    },
    section: {
      marginBottom: theme.spacing.xl,
    },
    sectionTitle: {
      fontSize: theme.typography.fontSize.large,
      fontFamily: theme.typography.fontFamilyBold,
      color: theme.colors.text,
      marginBottom: theme.spacing.md,
      paddingHorizontal: theme.spacing.sm,
    },
    settingItem: {
      flexDirection: 'row',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: theme.spacing.md,
      backgroundColor: theme.colors.backgroundCard,
      borderRadius: theme.borderRadius.medium,
      marginBottom: theme.spacing.sm,
      ...theme.shadows.small,
    },
    settingLeft: {
      flex: 1,
      flexDirection: 'row',
      alignItems: 'center',
    },
    settingIcon: {
      width: 40,
      height: 40,
      borderRadius: theme.borderRadius.round,
      backgroundColor: theme.colors.primaryLight,
      justifyContent: 'center',
      alignItems: 'center',
      marginRight: theme.spacing.md,
    },
    settingText: {
      flex: 1,
      fontSize: theme.typography.fontSize.medium,
      fontFamily: theme.typography.fontFamily,
      color: theme.colors.text,
    },
    settingValue: {
      fontSize: theme.typography.fontSize.small,
      fontFamily: theme.typography.fontFamily,
      color: theme.colors.textSecondary,
      marginTop: 2,
    },
    optionButton: {
      paddingVertical: theme.spacing.sm,
      paddingHorizontal: theme.spacing.md,
      borderRadius: theme.borderRadius.small,
      marginHorizontal: 2,
    },
    optionButtonActive: {
      backgroundColor: theme.colors.primary,
    },
    optionButtonInactive: {
      backgroundColor: theme.colors.backgroundSecondary,
    },
    optionButtonText: {
      fontSize: theme.typography.fontSize.small,
      fontFamily: theme.typography.fontFamilyBold,
    },
    optionButtonTextActive: {
      color: theme.colors.textInverse,
    },
    optionButtonTextInactive: {
      color: theme.colors.text,
    },
    optionsContainer: {
      flexDirection: 'row',
      flexWrap: 'wrap',
      marginTop: theme.spacing.sm,
    },
    resetButton: {
      marginTop: theme.spacing.xl,
      backgroundColor: theme.colors.error,
    },
  });
  
  const renderSettingItem = (icon, title, subtitle, action, value) => (
    <View style={styles.settingItem}>
      <View style={styles.settingLeft}>
        <View style={styles.settingIcon}>
          <Icon name={icon} size={20} color={theme.colors.primary} />
        </View>
        <View>
          <Text style={styles.settingText}>{title}</Text>
          {subtitle && <Text style={styles.settingValue}>{subtitle}</Text>}
        </View>
      </View>
      {action}
    </View>
  );
  
  const renderSwitch = (value, onValueChange) => (
    <Switch
      value={value}
      onValueChange={onValueChange}
      trackColor={{ false: theme.colors.border, true: theme.colors.primaryLight }}
      thumbColor={value ? theme.colors.primary : theme.colors.textLight}
    />
  );
  
  const renderOptionButton = (label, value, currentValue, onPress) => (
    <TouchableOpacity
      style={[
        styles.optionButton,
        value === currentValue ? styles.optionButtonActive : styles.optionButtonInactive,
      ]}
      onPress={() => onPress(value)}
    >
      <Text
        style={[
          styles.optionButtonText,
          value === currentValue ? styles.optionButtonTextActive : styles.optionButtonTextInactive,
        ]}
      >
        {label}
      </Text>
    </TouchableOpacity>
  );
  
  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      {/* Accessibility Settings */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Достъпност</Text>
        
        {renderSettingItem(
          'text-fields',
          'Размер на шрифта',
          'Настройте размера на текста',
          <View style={styles.optionsContainer}>
            {renderOptionButton('Малък', 'small', settings.fontSize, (value) => dispatch(setFontSize(value)))}
            {renderOptionButton('Среден', 'medium', settings.fontSize, (value) => dispatch(setFontSize(value)))}
            {renderOptionButton('Голям', 'large', settings.fontSize, (value) => dispatch(setFontSize(value)))}
            {renderOptionButton('Много голям', 'xlarge', settings.fontSize, (value) => dispatch(setFontSize(value)))}
          </View>
        )}
        
        {renderSettingItem(
          'contrast',
          'Висок контраст',
          'Подобрява четливостта',
          renderSwitch(settings.highContrast, () => dispatch(toggleHighContrast()))
        )}
        
        {renderSettingItem(
          'accessibility',
          'Намали анимациите',
          'За играчи с чувствителност към движение',
          renderSwitch(settings.reduceMotion, () => dispatch(toggleReduceMotion()))
        )}
        
        {renderSettingItem(
          'volume-up',
          'Звук',
          'Включи/изключи звуковите ефекти',
          renderSwitch(settings.soundEnabled, () => dispatch(toggleSound()))
        )}
        
        {renderSettingItem(
          'vibration',
          'Вибрации',
          'Тактилна обратна връзка',
          renderSwitch(settings.hapticFeedback, () => dispatch(toggleHapticFeedback()))
        )}
      </View>
      
      {/* Visual Settings */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Визуални настройки</Text>
        
        {renderSettingItem(
          'palette',
          'Тема',
          'Изберете светла или тъмна тема',
          <View style={styles.optionsContainer}>
            {renderOptionButton('Светла', 'light', settings.theme, (value) => dispatch(setTheme(value)))}
            {renderOptionButton('Тъмна', 'dark', settings.theme, (value) => dispatch(setTheme(value)))}
            {renderOptionButton('Авто', 'auto', settings.theme, (value) => dispatch(setTheme(value)))}
          </View>
        )}
      </View>
      
      {/* Game Settings */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Настройки на играта</Text>
        
        {renderSettingItem(
          'speed',
          'Трудност',
          'Автоматично или ръчно настройване',
          <View style={styles.optionsContainer}>
            {renderOptionButton('Авто', 'auto', settings.difficulty, (value) => dispatch(setDifficulty(value)))}
            {renderOptionButton('Лесно', 'easy', settings.difficulty, (value) => dispatch(setDifficulty(value)))}
            {renderOptionButton('Средно', 'medium', settings.difficulty, (value) => dispatch(setDifficulty(value)))}
            {renderOptionButton('Трудно', 'hard', settings.difficulty, (value) => dispatch(setDifficulty(value)))}
          </View>
        )}
      </View>
      
      {/* Reset Button */}
      <Button
        title="Нулирай настройките"
        onPress={handleResetSettings}
        variant="error"
        style={styles.resetButton}
      />
    </ScrollView>
  );
};

export default SettingsScreen; 