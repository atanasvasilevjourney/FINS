import React from 'react';
import { createStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { useSelector } from 'react-redux';
import Icon from 'react-native-vector-icons/MaterialIcons';

// Screens
import WelcomeScreen from '../screens/WelcomeScreen';
import GameScreen from '../screens/GameScreen';
import SettingsScreen from '../screens/SettingsScreen';
import ProfileScreen from '../screens/ProfileScreen';
import LeaderboardScreen from '../screens/LeaderboardScreen';
import ThemeSelectionScreen from '../screens/ThemeSelectionScreen';
import TutorialScreen from '../screens/TutorialScreen';
import AchievementScreen from '../screens/AchievementScreen';
import StatisticsScreen from '../screens/StatisticsScreen';

// Components
import { useTheme } from '../context/ThemeContext';

const Stack = createStackNavigator();
const Tab = createBottomTabNavigator();

const MainTabNavigator = () => {
  const theme = useTheme();
  
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          let iconName;
          
          switch (route.name) {
            case 'Game':
              iconName = 'extension';
              break;
            case 'Profile':
              iconName = 'person';
              break;
            case 'Leaderboard':
              iconName = 'leaderboard';
              break;
            case 'Settings':
              iconName = 'settings';
              break;
            default:
              iconName = 'help';
          }
          
          return <Icon name={iconName} size={size} color={color} />;
        },
        tabBarActiveTintColor: theme.colors.primary,
        tabBarInactiveTintColor: theme.colors.textSecondary,
        tabBarStyle: {
          backgroundColor: theme.colors.backgroundCard,
          borderTopColor: theme.colors.border,
          borderTopWidth: 1,
          paddingBottom: 8,
          paddingTop: 8,
          height: 60,
        },
        tabBarLabelStyle: {
          fontSize: theme.typography.fontSize.small,
          fontFamily: theme.typography.fontFamily,
        },
        headerStyle: {
          backgroundColor: theme.colors.backgroundCard,
          borderBottomColor: theme.colors.border,
          borderBottomWidth: 1,
        },
        headerTintColor: theme.colors.text,
        headerTitleStyle: {
          fontFamily: theme.typography.fontFamilyBold,
          fontSize: theme.typography.fontSize.large,
        },
      })}
    >
      <Tab.Screen 
        name="Game" 
        component={GameScreen}
        options={{
          title: 'Игра',
          headerShown: false,
        }}
      />
      <Tab.Screen 
        name="Profile" 
        component={ProfileScreen}
        options={{
          title: 'Профил',
        }}
      />
      <Tab.Screen 
        name="Leaderboard" 
        component={LeaderboardScreen}
        options={{
          title: 'Класация',
        }}
      />
      <Tab.Screen 
        name="Settings" 
        component={SettingsScreen}
        options={{
          title: 'Настройки',
        }}
      />
    </Tab.Navigator>
  );
};

const AppNavigator = () => {
  const user = useSelector(state => state.user);
  const theme = useTheme();
  
  return (
    <Stack.Navigator
      screenOptions={{
        headerStyle: {
          backgroundColor: theme.colors.backgroundCard,
          borderBottomColor: theme.colors.border,
          borderBottomWidth: 1,
        },
        headerTintColor: theme.colors.text,
        headerTitleStyle: {
          fontFamily: theme.typography.fontFamilyBold,
          fontSize: theme.typography.fontSize.large,
        },
        cardStyle: {
          backgroundColor: theme.colors.background,
        },
      }}
    >
      {!user.id ? (
        // Auth screens
        <>
          <Stack.Screen 
            name="Welcome" 
            component={WelcomeScreen}
            options={{ headerShown: false }}
          />
          <Stack.Screen 
            name="Tutorial" 
            component={TutorialScreen}
            options={{ 
              title: 'Как да играете',
              headerBackTitle: 'Назад'
            }}
          />
        </>
      ) : (
        // Main app screens
        <>
          <Stack.Screen 
            name="MainTabs" 
            component={MainTabNavigator}
            options={{ headerShown: false }}
          />
          <Stack.Screen 
            name="ThemeSelection" 
            component={ThemeSelectionScreen}
            options={{ 
              title: 'Избор на тема',
              headerBackTitle: 'Назад'
            }}
          />
          <Stack.Screen 
            name="Achievements" 
            component={AchievementScreen}
            options={{ 
              title: 'Постижения',
              headerBackTitle: 'Назад'
            }}
          />
          <Stack.Screen 
            name="Statistics" 
            component={StatisticsScreen}
            options={{ 
              title: 'Статистики',
              headerBackTitle: 'Назад'
            }}
          />
        </>
      )}
    </Stack.Navigator>
  );
};

export default AppNavigator; 