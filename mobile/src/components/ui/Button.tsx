/**
 * Button Component for MicroLearning Platform
 * 
 * Age-adaptive button component with proper touch targets
 * and accessibility features for educational content
 */

import React from 'react';
import {
  TouchableOpacity,
  Text,
  ViewStyle,
  TextStyle,
  ActivityIndicator,
  Animated,
} from 'react-native';
import { Colors, Typography, ComponentVariants, AgeGroups, type AgeGroup } from './DesignSystem';

interface ButtonProps {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  ageGroup?: AgeGroup;
  disabled?: boolean;
  loading?: boolean;
  fullWidth?: boolean;
  onPress?: () => void;
  style?: ViewStyle;
  textStyle?: TextStyle;
  testID?: string;
  accessibilityLabel?: string;
  accessibilityHint?: string;
}

export const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  ageGroup = '12-15',
  disabled = false,
  loading = false,
  fullWidth = false,
  onPress,
  style,
  textStyle,
  testID,
  accessibilityLabel,
  accessibilityHint,
}) => {
  const scaleValue = React.useRef(new Animated.Value(1)).current;
  const ageConfig = AgeGroups[ageGroup];
  
  // Get size configuration
  const sizeConfig = ComponentVariants.button.sizes[size];
  const variantConfig = ComponentVariants.button.variants[variant];
  
  // Apply age-specific adjustments
  const adjustedPaddingVertical = sizeConfig.paddingVertical * ageConfig.spacing;
  const adjustedPaddingHorizontal = sizeConfig.paddingHorizontal * ageConfig.spacing;
  const adjustedFontSize = sizeConfig.fontSize * ageConfig.fontSize;
  const adjustedTouchTarget = Math.max(ageConfig.touchTargetSize, sizeConfig.paddingVertical * 2 + adjustedFontSize);
  
  // Animation handlers
  const handlePressIn = () => {
    Animated.spring(scaleValue, {
      toValue: 0.95,
      useNativeDriver: true,
      tension: 300,
      friction: 10,
    }).start();
  };

  const handlePressOut = () => {
    Animated.spring(scaleValue, {
      toValue: 1,
      useNativeDriver: true,
      tension: 300,
      friction: 10,
    }).start();
  };

  const handlePress = () => {
    if (!disabled && !loading && onPress) {
      onPress();
    }
  };

  // Determine colors based on state
  const getBackgroundColor = () => {
    if (disabled) return Colors.interactive.disabled;
    if (variant === 'outline' || variant === 'ghost') return variantConfig.backgroundColor;
    return ageConfig.colors.primary;
  };

  const getTextColor = () => {
    if (disabled) return Colors.neutral.textSecondary;
    if (variant === 'outline' || variant === 'ghost') return ageConfig.colors.primary;
    return variantConfig.color;
  };

  const getBorderColor = () => {
    if (variant === 'outline') {
      return disabled ? Colors.interactive.disabled : ageConfig.colors.primary;
    }
    return 'transparent';
  };

  const buttonStyle: ViewStyle = {
    paddingVertical: adjustedPaddingVertical,
    paddingHorizontal: adjustedPaddingHorizontal,
    borderRadius: sizeConfig.borderRadius,
    backgroundColor: getBackgroundColor(),
    borderWidth: variant === 'outline' ? 2 : 0,
    borderColor: getBorderColor(),
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: adjustedTouchTarget,
    width: fullWidth ? '100%' : 'auto',
    opacity: disabled ? 0.6 : 1,
    ...style,
  };

  const buttonTextStyle: TextStyle = {
    fontSize: adjustedFontSize,
    fontWeight: Typography.weights.semibold,
    color: getTextColor(),
    textAlign: 'center',
    ...textStyle,
  };

  return (
    <Animated.View style={{ transform: [{ scale: scaleValue }] }}>
      <TouchableOpacity
        style={buttonStyle}
        onPress={handlePress}
        onPressIn={handlePressIn}
        onPressOut={handlePressOut}
        disabled={disabled || loading}
        activeOpacity={0.8}
        testID={testID}
        accessibilityRole="button"
        accessibilityLabel={accessibilityLabel}
        accessibilityHint={accessibilityHint}
        accessibilityState={{
          disabled: disabled || loading,
          busy: loading,
        }}
      >
        {loading ? (
          <ActivityIndicator 
            size="small" 
            color={getTextColor()} 
          />
        ) : (
          <Text style={buttonTextStyle}>
            {children}
          </Text>
        )}
      </TouchableOpacity>
    </Animated.View>
  );
};

// Specialized button variants for common use cases
export const QuizButton: React.FC<Omit<ButtonProps, 'variant'> & {
  isCorrect?: boolean;
  showFeedback?: boolean;
}> = ({ isCorrect, showFeedback, style, ...props }) => {
  const feedbackStyle: ViewStyle = showFeedback ? {
    backgroundColor: isCorrect ? Colors.interactive.correct : Colors.interactive.incorrect,
  } : {};

  return (
    <Button
      variant="primary"
      style={{ ...feedbackStyle, ...style }}
      {...props}
    />
  );
};

export const BinaryChoiceButton: React.FC<Omit<ButtonProps, 'variant' | 'size'> & {
  choice: 'yes' | 'no';
  zone: 'left' | 'right';
}> = ({ choice, zone, style, children, ...props }) => {
  const zoneStyle: ViewStyle = {
    flex: 1,
    backgroundColor: choice === 'yes' ? Colors.interactive.correct : Colors.interactive.incorrect,
    margin: 4,
    ...style,
  };

  return (
    <Button
      variant="primary"
      size="lg"
      style={zoneStyle}
      {...props}
    >
      {children}
    </Button>
  );
};

export const ActionButton: React.FC<Omit<ButtonProps, 'variant'> & {
  icon?: React.ReactNode;
  iconPosition?: 'left' | 'right';
}> = ({ icon, iconPosition = 'left', children, style, ...props }) => {
  return (
    <Button
      variant="secondary"
      style={{
        flexDirection: 'row',
        alignItems: 'center',
        gap: 8,
        ...style,
      }}
      {...props}
    >
      {icon && iconPosition === 'left' && icon}
      {children}
      {icon && iconPosition === 'right' && icon}
    </Button>
  );
};