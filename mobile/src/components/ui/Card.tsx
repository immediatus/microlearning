/**
 * Card Component for MicroLearning Platform
 * 
 * Flexible card component for displaying content, progress,
 * and interactive elements with age-appropriate styling
 */

import React from 'react';
import {
  View,
  ViewStyle,
  TouchableOpacity,
  Animated,
} from 'react-native';
import { Colors, Spacing, BorderRadius, Shadows, ComponentVariants, AgeGroups, type AgeGroup } from './DesignSystem';

interface CardProps {
  children: React.ReactNode;
  variant?: 'default' | 'elevated' | 'flat';
  ageGroup?: AgeGroup;
  interactive?: boolean;
  onPress?: () => void;
  style?: ViewStyle;
  testID?: string;
  accessibilityLabel?: string;
  accessibilityHint?: string;
}

export const Card: React.FC<CardProps> = ({
  children,
  variant = 'default',
  ageGroup = '12-15',
  interactive = false,
  onPress,
  style,
  testID,
  accessibilityLabel,
  accessibilityHint,
}) => {
  const scaleValue = React.useRef(new Animated.Value(1)).current;
  const ageConfig = AgeGroups[ageGroup];
  const variantConfig = ComponentVariants.card.variants[variant];
  
  // Apply age-specific adjustments
  const adjustedPadding = variantConfig.padding * ageConfig.spacing;
  const adjustedBorderRadius = variantConfig.borderRadius * ageConfig.spacing;
  
  // Animation handlers for interactive cards
  const handlePressIn = () => {
    if (interactive) {
      Animated.spring(scaleValue, {
        toValue: 0.98,
        useNativeDriver: true,
        tension: 300,
        friction: 10,
      }).start();
    }
  };

  const handlePressOut = () => {
    if (interactive) {
      Animated.spring(scaleValue, {
        toValue: 1,
        useNativeDriver: true,
        tension: 300,
        friction: 10,
      }).start();
    }
  };

  const cardStyle: ViewStyle = {
    backgroundColor: variantConfig.backgroundColor,
    borderRadius: adjustedBorderRadius,
    padding: adjustedPadding,
    ...variantConfig,
    ...style,
  };

  const CardWrapper = interactive ? TouchableOpacity : View;

  return (
    <Animated.View style={{ transform: [{ scale: scaleValue }] }}>
      <CardWrapper
        style={cardStyle}
        onPress={onPress}
        onPressIn={handlePressIn}
        onPressOut={handlePressOut}
        activeOpacity={interactive ? 0.95 : 1}
        testID={testID}
        accessibilityRole={interactive ? "button" : "none"}
        accessibilityLabel={accessibilityLabel}
        accessibilityHint={accessibilityHint}
      >
        {children}
      </CardWrapper>
    </Animated.View>
  );
};

// Specialized card variants
export const VideoCard: React.FC<Omit<CardProps, 'variant'> & {
  thumbnail?: string;
  duration?: number;
  progress?: number;
  title?: string;
}> = ({ thumbnail, duration, progress, title, children, ...props }) => {
  return (
    <Card
      variant="elevated"
      interactive={true}
      style={{
        overflow: 'hidden',
        aspectRatio: 9 / 16, // TikTok-style aspect ratio
      }}
      {...props}
    >
      {children}
      {/* Progress indicator */}
      {progress !== undefined && (
        <View style={{
          position: 'absolute',
          bottom: 0,
          left: 0,
          right: 0,
          height: 4,
          backgroundColor: Colors.neutral.border,
        }}>
          <View style={{
            width: `${progress * 100}%`,
            height: '100%',
            backgroundColor: Colors.primary.teal,
          }} />
        </View>
      )}
    </Card>
  );
};

export const ProgressCard: React.FC<Omit<CardProps, 'variant'> & {
  title: string;
  progress: number;
  total: number;
  color?: string;
}> = ({ title, progress, total, color = Colors.primary.teal, children, style, ...props }) => {
  const progressPercentage = Math.min((progress / total) * 100, 100);
  
  return (
    <Card
      variant="flat"
      style={{
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
        ...style,
      }}
      {...props}
    >
      <View style={{ flex: 1 }}>
        {children}
        {/* Progress bar */}
        <View style={{
          marginTop: Spacing.sm,
          height: 8,
          backgroundColor: Colors.neutral.border,
          borderRadius: BorderRadius.round,
          overflow: 'hidden',
        }}>
          <Animated.View style={{
            width: `${progressPercentage}%`,
            height: '100%',
            backgroundColor: color,
            borderRadius: BorderRadius.round,
          }} />
        </View>
      </View>
    </Card>
  );
};

export const AchievementCard: React.FC<Omit<CardProps, 'variant'> & {
  earned?: boolean;
  icon?: React.ReactNode;
  title: string;
  description: string;
}> = ({ earned = false, icon, title, description, style, ...props }) => {
  return (
    <Card
      variant="elevated"
      style={{
        alignItems: 'center',
        opacity: earned ? 1 : 0.6,
        borderWidth: earned ? 2 : 0,
        borderColor: earned ? Colors.primary.orange : 'transparent',
        ...style,
      }}
      {...props}
    >
      {/* Icon */}
      <View style={{
        width: 64,
        height: 64,
        borderRadius: BorderRadius.round,
        backgroundColor: earned ? Colors.primary.orange : Colors.neutral.border,
        alignItems: 'center',
        justifyContent: 'center',
        marginBottom: Spacing.md,
      }}>
        {icon}
      </View>
      
      {/* Content */}
      <View style={{ alignItems: 'center' }}>
        {/* Title and description would be Text components */}
      </View>
    </Card>
  );
};

export const QuizQuestionCard: React.FC<Omit<CardProps, 'variant'> & {
  questionNumber: number;
  totalQuestions: number;
  timeLeft?: number;
  maxTime?: number;
}> = ({ 
  questionNumber, 
  totalQuestions, 
  timeLeft, 
  maxTime = 5000,
  children, 
  style,
  ...props 
}) => {
  const timeProgress = timeLeft ? (timeLeft / maxTime) : 0;
  
  return (
    <Card
      variant="elevated"
      style={{
        margin: Spacing.md,
        ...style,
      }}
      {...props}
    >
      {/* Question progress */}
      <View style={{
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: Spacing.md,
      }}>
        {/* Question counter */}
        <View style={{
          backgroundColor: Colors.primary.blue,
          paddingHorizontal: Spacing.sm,
          paddingVertical: Spacing.xs,
          borderRadius: BorderRadius.md,
        }}>
          {/* Text component would go here */}
        </View>
        
        {/* Timer */}
        {timeLeft !== undefined && (
          <View style={{
            width: 40,
            height: 40,
            borderRadius: BorderRadius.round,
            backgroundColor: Colors.neutral.border,
            alignItems: 'center',
            justifyContent: 'center',
            position: 'relative',
          }}>
            {/* Circular progress indicator */}
            <View style={{
              position: 'absolute',
              width: '100%',
              height: '100%',
              borderRadius: BorderRadius.round,
              borderWidth: 3,
              borderColor: timeProgress > 0.3 ? Colors.primary.teal : Colors.primary.red,
              borderTopColor: 'transparent',
              transform: [{ rotate: `${(1 - timeProgress) * 360}deg` }],
            }} />
          </View>
        )}
      </View>
      
      {/* Question content */}
      {children}
    </Card>
  );
};