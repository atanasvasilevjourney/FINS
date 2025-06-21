import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
} from 'react-native';
import { useSelector } from 'react-redux';
import { useTheme } from '../context/ThemeContext';
import { useNavigation } from '@react-navigation/native';
import Icon from 'react-native-vector-icons/MaterialIcons';

const ProfileScreen = () => {
  const navigation = useNavigation();
  const theme = useTheme();
  const { profile, achievements, unlockedThemes } = useSelector(state => state.user);
  
  const styles = StyleSheet.create({
    container: {
      flex: 1,
      backgroundColor: theme.colors.background,
    },
    content: {
      padding: theme.spacing.md,
    },
    header: {
      alignItems: 'center',
      padding: theme.spacing.lg,
      backgroundColor: theme.colors.backgroundCard,
      borderRadius: theme.borderRadius.large,
      marginBottom: theme.spacing.lg,
      ...theme.shadows.medium,
    },
    avatar: {
      width: 80,
      height: 80,
      borderRadius: theme.borderRadius.round,
      backgroundColor: theme.colors.primary,
      justifyContent: 'center',
      alignItems: 'center',
      marginBottom: theme.spacing.md,
    },
    avatarText: {
      fontSize: 32,
      fontFamily: theme.typography.fontFamilyBold,
      color: theme.colors.textInverse,
    },
    username: {
      fontSize: theme.typography.fontSize.title,
      fontFamily: theme.typography.fontFamilyBold,
      color: theme.colors.text,
      marginBottom: theme.spacing.xs,
    },
    level: {
      fontSize: theme.typography.fontSize.medium,
      fontFamily: theme.typography.fontFamily,
      color: theme.colors.primary,
      marginBottom: theme.spacing.sm,
    },
    stats: {
      flexDirection: 'row',
      justifyContent: 'space-around',
      width: '100%',
    },
    statItem: {
      alignItems: 'center',
    },
    statValue: {
      fontSize: theme.typography.fontSize.large,
      fontFamily: theme.typography.fontFamilyBold,
      color: theme.colors.text,
    },
    statLabel: {
      fontSize: theme.typography.fontSize.small,
      fontFamily: theme.typography.fontFamily,
      color: theme.colors.textSecondary,
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
    statCard: {
      backgroundColor: theme.colors.backgroundCard,
      padding: theme.spacing.md,
      borderRadius: theme.borderRadius.medium,
      marginBottom: theme.spacing.sm,
      ...theme.shadows.small,
    },
    statRow: {
      flexDirection: 'row',
      justifyContent: 'space-between',
      alignItems: 'center',
      marginBottom: theme.spacing.sm,
    },
    statRowLast: {
      marginBottom: 0,
    },
    statName: {
      fontSize: theme.typography.fontSize.medium,
      fontFamily: theme.typography.fontFamily,
      color: theme.colors.text,
    },
    statValue: {
      fontSize: theme.typography.fontSize.medium,
      fontFamily: theme.typography.fontFamilyBold,
      color: theme.colors.primary,
    },
    achievementItem: {
      flexDirection: 'row',
      alignItems: 'center',
      padding: theme.spacing.md,
      backgroundColor: theme.colors.backgroundCard,
      borderRadius: theme.borderRadius.medium,
      marginBottom: theme.spacing.sm,
      ...theme.shadows.small,
    },
    achievementIcon: {
      width: 50,
      height: 50,
      borderRadius: theme.borderRadius.round,
      backgroundColor: theme.colors.success,
      justifyContent: 'center',
      alignItems: 'center',
      marginRight: theme.spacing.md,
    },
    achievementText: {
      flex: 1,
    },
    achievementTitle: {
      fontSize: theme.typography.fontSize.medium,
      fontFamily: theme.typography.fontFamilyBold,
      color: theme.colors.text,
      marginBottom: 2,
    },
    achievementDate: {
      fontSize: theme.typography.fontSize.small,
      fontFamily: theme.typography.fontFamily,
      color: theme.colors.textSecondary,
    },
    actionButton: {
      flexDirection: 'row',
      alignItems: 'center',
      padding: theme.spacing.md,
      backgroundColor: theme.colors.backgroundCard,
      borderRadius: theme.borderRadius.medium,
      marginBottom: theme.spacing.sm,
      ...theme.shadows.small,
    },
    actionButtonText: {
      flex: 1,
      fontSize: theme.typography.fontSize.medium,
      fontFamily: theme.typography.fontFamily,
      color: theme.colors.text,
      marginLeft: theme.spacing.md,
    },
    emptyState: {
      alignItems: 'center',
      padding: theme.spacing.xl,
    },
    emptyText: {
      fontSize: theme.typography.fontSize.medium,
      fontFamily: theme.typography.fontFamily,
      color: theme.colors.textSecondary,
      textAlign: 'center',
    },
  });
  
  const formatTime = (seconds) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    return `${hours}ч ${minutes}м`;
  };
  
  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('bg-BG');
  };
  
  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      {/* Profile Header */}
      <View style={styles.header}>
        <View style={styles.avatar}>
          <Text style={styles.avatarText}>
            {profile.username.charAt(0).toUpperCase()}
          </Text>
        </View>
        
        <Text style={styles.username}>{profile.username}</Text>
        <Text style={styles.level}>Ниво {profile.level}</Text>
        
        <View style={styles.stats}>
          <View style={styles.statItem}>
            <Text style={styles.statValue}>{profile.totalPoints}</Text>
            <Text style={styles.statLabel}>Точки</Text>
          </View>
          <View style={styles.statItem}>
            <Text style={styles.statValue}>{profile.gamesCompleted}</Text>
            <Text style={styles.statLabel}>Игри</Text>
          </View>
          <View style={styles.statItem}>
            <Text style={styles.statValue}>{profile.currentStreak}</Text>
            <Text style={styles.statLabel}>Серия</Text>
          </View>
        </View>
      </View>
      
      {/* Statistics */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Статистики</Text>
        
        <View style={styles.statCard}>
          <View style={styles.statRow}>
            <Text style={styles.statName}>Общо игри</Text>
            <Text style={styles.statValue}>{profile.gamesPlayed}</Text>
          </View>
          <View style={styles.statRow}>
            <Text style={styles.statName}>Завършени игри</Text>
            <Text style={styles.statValue}>{profile.gamesCompleted}</Text>
          </View>
          <View style={styles.statRow}>
            <Text style={styles.statName}>Време за игра</Text>
            <Text style={styles.statValue}>{formatTime(profile.totalTimePlayed)}</Text>
          </View>
          <View style={styles.statRow}>
            <Text style={styles.statName}>Средна точност</Text>
            <Text style={styles.statValue}>{Math.round(profile.averageAccuracy * 100)}%</Text>
          </View>
          <View style={styles.statRow}>
            <Text style={styles.statName}>Средно време</Text>
            <Text style={styles.statValue}>{Math.round(profile.averageTime / 60)}м</Text>
          </View>
          <View style={styles.statRow}>
            <Text style={styles.statName}>Най-добра серия</Text>
            <Text style={styles.statValue}>{profile.longestStreak}</Text>
          </View>
        </View>
      </View>
      
      {/* Achievements */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Постижения</Text>
        
        {achievements.length > 0 ? (
          achievements.map((achievement, index) => (
            <View key={index} style={styles.achievementItem}>
              <View style={styles.achievementIcon}>
                <Icon name="emoji-events" size={24} color={theme.colors.textInverse} />
              </View>
              <View style={styles.achievementText}>
                <Text style={styles.achievementTitle}>{achievement.achievement_type}</Text>
                <Text style={styles.achievementDate}>
                  {formatDate(achievement.unlocked_at)}
                </Text>
              </View>
            </View>
          ))
        ) : (
          <View style={styles.emptyState}>
            <Text style={styles.emptyText}>
              Все още нямате постижения.{'\n'}
              Играйте повече за да ги отключите!
            </Text>
          </View>
        )}
      </View>
      
      {/* Actions */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Действия</Text>
        
        <TouchableOpacity
          style={styles.actionButton}
          onPress={() => navigation.navigate('Statistics')}
        >
          <Icon name="analytics" size={24} color={theme.colors.primary} />
          <Text style={styles.actionButtonText}>Подробни статистики</Text>
          <Icon name="chevron-right" size={24} color={theme.colors.textSecondary} />
        </TouchableOpacity>
        
        <TouchableOpacity
          style={styles.actionButton}
          onPress={() => navigation.navigate('Achievements')}
        >
          <Icon name="emoji-events" size={24} color={theme.colors.primary} />
          <Text style={styles.actionButtonText}>Всички постижения</Text>
          <Icon name="chevron-right" size={24} color={theme.colors.textSecondary} />
        </TouchableOpacity>
        
        <TouchableOpacity
          style={styles.actionButton}
          onPress={() => navigation.navigate('ThemeSelection')}
        >
          <Icon name="palette" size={24} color={theme.colors.primary} />
          <Text style={styles.actionButtonText}>Избор на тема</Text>
          <Icon name="chevron-right" size={24} color={theme.colors.textSecondary} />
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
};

export default ProfileScreen; 