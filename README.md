# Кръстословица+ (Bulgarian Crossword Plus)

A fully functional Bulgarian Crossword Puzzle Game built with React Native for Android and iOS, specifically designed for Bulgarian-speaking adults 55+ with accessibility-first design principles.

## 🎯 Project Overview

**Кръстословица+** is a cognitive stimulation game that combines traditional crossword puzzles with modern mobile technology, featuring:

- **Bulgarian Language Support**: Full Cyrillic alphabet support with proper Bulgarian words and themes
- **Accessibility-First Design**: Optimized for elderly users with large fonts, high contrast, and reduced motion
- **Cognitive Training**: Progressive difficulty system to challenge and improve memory and logical thinking
- **Cultural Engagement**: Bulgarian-themed content including cities, nature, food, proverbs, and history
- **Social Features**: Leaderboards and achievements for community engagement

## 🚀 Features

### Core Gameplay
- **Interactive Crossword Grid**: Touch-based letter selection and word building
- **Bulgarian Dictionary**: 1000+ Bulgarian words with proper validation
- **Themed Puzzles**: Nature, Cities, Food, Proverbs, History, Sports
- **Progressive Difficulty**: 5 difficulty levels with adaptive learning
- **Daily Challenges**: New puzzles every day with consistent seeds

### Accessibility Features
- **Adjustable Font Sizes**: Small, Medium, Large, Extra Large
- **High Contrast Mode**: Enhanced visibility for users with visual impairments
- **Reduced Motion**: Respects user's motion sensitivity preferences
- **Haptic Feedback**: Tactile response for better interaction
- **Voice Over Support**: Screen reader compatibility
- **Large Touch Targets**: Minimum 44px touch areas for easy interaction

### User Experience
- **Light/Dark Theme**: Automatic theme switching based on system preferences
- **Offline Support**: Play without internet connection
- **Progress Tracking**: Detailed statistics and achievements
- **Hint System**: Smart hints to help when stuck
- **Pause/Resume**: Save progress and continue later

### Technical Features
- **Cross-Platform**: Works on both Android and iOS
- **State Management**: Redux Toolkit with persistence
- **Performance Optimized**: Smooth animations and responsive UI
- **Modular Architecture**: Clean, maintainable code structure

## 📱 Screenshots

The app includes the following main screens:
- **Welcome Screen**: App introduction and tutorial access
- **Game Screen**: Main crossword puzzle interface
- **Profile Screen**: User statistics and achievements
- **Leaderboard**: Global rankings and competition
- **Settings**: Accessibility and game preferences
- **Tutorial**: Step-by-step game instructions

## 🛠️ Technical Stack

### Frontend
- **React Native 0.72.6**: Cross-platform mobile development
- **React Navigation 6**: Screen navigation and routing
- **Redux Toolkit**: State management with RTK Query
- **Redux Persist**: Offline data persistence

### UI/UX
- **Custom Theme System**: Light/dark themes with accessibility support
- **React Native Vector Icons**: Material Design icons
- **React Native Reanimated**: Smooth animations
- **React Native Gesture Handler**: Touch interactions

### Data & Storage
- **AsyncStorage**: Local data persistence
- **SQLite**: Offline database for puzzles and user data
- **Firebase** (planned): Backend services and analytics

### Development Tools
- **TypeScript**: Type safety and better development experience
- **ESLint & Prettier**: Code quality and formatting
- **Jest**: Unit testing framework

## 📦 Installation

### Prerequisites
- Node.js 16+ 
- React Native CLI
- Android Studio (for Android development)
- Xcode (for iOS development, macOS only)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/bulgarian-crossword-plus.git
   cd bulgarian-crossword-plus
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **iOS Setup** (macOS only)
   ```bash
   cd ios
   pod install
   cd ..
   ```

4. **Start the development server**
   ```bash
   npm start
   # or
   yarn start
   ```

5. **Run on device/simulator**
   ```bash
   # Android
   npm run android
   
   # iOS
   npm run ios
   ```

## ��️ Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── common/         # Generic components (Button, Input, etc.)
│   ├── game/           # Game-specific components
│   └── accessibility/  # Accessibility components
├── screens/            # App screens
├── navigation/         # Navigation configuration
├── store/              # Redux store and slices
├── services/           # API and business logic services
├── utils/              # Helper functions and utilities
├── data/               # Static data (words, themes, etc.)
├── context/            # React Context providers
└── assets/             # Images, fonts, sounds
```

## 🎮 Game Mechanics

### Word Selection
1. **Touch Letters**: Tap letters in the grid to select them
2. **Build Words**: Selected letters form words automatically
3. **Submit Words**: Confirm words to check against clues
4. **Earn Points**: Score based on word length, speed, and difficulty

### Scoring System
- **Base Points**: 10 points per letter
- **Time Bonus**: Faster completion = more points
- **Difficulty Multiplier**: Higher difficulty = more points
- **Hint Penalty**: Using hints reduces points
- **Perfect Solve Bonus**: Complete puzzles without hints

### Difficulty Levels
- **Level 1**: 7x7 grid, 5 words, easy themes
- **Level 2**: 9x9 grid, 7 words, moderate themes
- **Level 3**: 11x11 grid, 9 words, challenging themes
- **Level 4**: 13x13 grid, 12 words, expert themes
- **Level 5**: 15x15 grid, 15 words, master themes

## 🌍 Bulgarian Language Support

### Alphabet Support
Full support for the Bulgarian Cyrillic alphabet:
```
А Б В Г Д Е Ж З И Й К Л М Н О П Р С Т У Ф Х Ц Ч Ш Щ Ъ Ь Ю Я
```

### Word Categories
- **Nature**: гора, река, планина, цвете, дърво
- **Cities**: София, Пловдив, Варна, Бургас, Русе
- **Food**: баница, кебапче, лютеница, таратор
- **Proverbs**: търпение, мъдрост, доброта, честност
- **History**: хан, цар, бояр, войвода, патриарх
- **Sports**: футбол, волейбол, баскетбол, тенис

## ♿ Accessibility Features

### Visual Accessibility
- **High Contrast Mode**: Enhanced color contrast
- **Adjustable Font Sizes**: 4 size options (16px - 34px)
- **Dark/Light Themes**: Automatic system preference detection
- **Large Touch Targets**: Minimum 44px touch areas

### Motor Accessibility
- **Haptic Feedback**: Tactile response for interactions
- **Reduced Motion**: Respects user's motion preferences
- **Simple Gestures**: Tap-based interactions only
- **Pause/Resume**: Easy game interruption and continuation

### Cognitive Accessibility
- **Clear Instructions**: Step-by-step tutorial
- **Consistent UI**: Predictable interface patterns
- **Progress Indicators**: Clear feedback on game state
- **Error Prevention**: Confirmation dialogs for important actions

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:
```env
# Firebase Configuration (for future use)
FIREBASE_API_KEY=your_api_key
FIREBASE_AUTH_DOMAIN=your_auth_domain
FIREBASE_PROJECT_ID=your_project_id
FIREBASE_STORAGE_BUCKET=your_storage_bucket
FIREBASE_MESSAGING_SENDER_ID=your_sender_id
FIREBASE_APP_ID=your_app_id
```

### App Configuration
Edit `app.json` for app-specific settings:
```json
{
  "name": "BulgarianCrosswordPlus",
  "displayName": "Кръстословица+",
  "version": "1.0.0"
}
```

## 🧪 Testing

### Unit Tests
```bash
npm test
```

### E2E Tests (planned)
```bash
npm run test:e2e
```

### Accessibility Testing
- VoiceOver testing on iOS
- TalkBack testing on Android
- Color contrast validation
- Touch target size verification

## 📊 Analytics & Monitoring

### Firebase Analytics (planned)
- User engagement metrics
- Game completion rates
- Feature usage statistics
- Performance monitoring

### Crash Reporting
- Automatic crash detection
- Error logging and reporting
- Performance monitoring

## 🚀 Deployment

### Android
1. **Build APK**
   ```bash
   cd android
   ./gradlew assembleRelease
   ```

2. **Build AAB** (for Google Play Store)
   ```bash
   cd android
   ./gradlew bundleRelease
   ```

### iOS
1. **Archive for App Store**
   ```bash
   cd ios
   xcodebuild -workspace BulgarianCrosswordPlus.xcworkspace -scheme BulgarianCrosswordPlus -configuration Release archive
   ```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Workflow
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

### Code Style
- Follow the existing code style
- Use TypeScript for new files
- Add JSDoc comments for functions
- Write meaningful commit messages

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Bulgarian Language Institute**: For word validation and cultural accuracy
- **React Native Community**: For the excellent framework and tools
- **Accessibility Advocates**: For guidance on inclusive design
- **Beta Testers**: For valuable feedback and testing

## 📞 Support

For support and questions:
- **Email**: support@bulgariancrossword.com
- **Issues**: [GitHub Issues](https://github.com/your-username/bulgarian-crossword-plus/issues)
- **Documentation**: [Wiki](https://github.com/your-username/bulgarian-crossword-plus/wiki)

## 🔮 Roadmap

### Version 1.1 (Q2 2024)
- [ ] Firebase backend integration
- [ ] User authentication
- [ ] Cloud save/restore
- [ ] Social features (friends, challenges)

### Version 1.2 (Q3 2024)
- [ ] Advanced puzzle generation
- [ ] Custom puzzle creation
- [ ] Multiplayer mode
- [ ] Voice commands

### Version 1.3 (Q4 2024)
- [ ] AI-powered difficulty adjustment
- [ ] Personalized recommendations
- [ ] Advanced analytics
- [ ] Premium features

---

**Made with ❤️ for the Bulgarian community**
