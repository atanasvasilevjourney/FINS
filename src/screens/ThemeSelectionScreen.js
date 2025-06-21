import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { useTheme } from '../context/ThemeContext';

const ThemeSelectionScreen = () => {
  const theme = useTheme();
  
  const styles = StyleSheet.create({
    container: {
      flex: 1,
      justifyContent: 'center',
      alignItems: 'center',
      backgroundColor: theme.colors.background,
      padding: theme.spacing.lg,
    },
    text: {
      fontSize: theme.typography.fontSize.large,
      fontFamily: theme.typography.fontFamily,
      color: theme.colors.text,
      textAlign: 'center',
    },
  });
  
  return (
    <View style={styles.container}>
      <Text style={styles.text}>
        Избор на тема{'\n'}
        (Функционалност в разработка)
      </Text>
    </View>
  );
};

export default ThemeSelectionScreen; 