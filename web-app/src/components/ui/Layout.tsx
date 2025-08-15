import React from 'react';
import { cn } from '../../lib/utils';
import { spacing } from '../../lib/design-system';

// Container Component
export interface ContainerProps extends React.HTMLAttributes<HTMLDivElement> {}

const Container = React.forwardRef<HTMLDivElement, ContainerProps>(
  ({ className, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(
          'w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8',
          className
        )}
        {...props}
      />
    );
  }
);
Container.displayName = 'Container';

// Grid Component
export interface GridProps extends React.HTMLAttributes<HTMLDivElement> {
  cols?: number;
  gap?: keyof typeof spacing;
}

const Grid = React.forwardRef<HTMLDivElement, GridProps>(
  ({ className, cols = 1, gap = 'md', ...props }, ref) => {
    // Note: This requires Tailwind JIT to be enabled to generate dynamic classes like grid-cols-5.
    // For AOT compilation, you might need to safelist these classes.
    const gridColsClass = `grid-cols-${cols}`;
    const gapClass = `gap-${spacing[gap]}`;

    return (
      <div
        ref={ref}
        className={cn('grid', gridColsClass, gapClass, className)}
        {...props}
      />
    );
  }
);
Grid.displayName = 'Grid';


// Flex Component
export interface FlexProps extends React.HTMLAttributes<HTMLDivElement> {
  justify?: 'start' | 'center' | 'end' | 'between' | 'around';
  align?: 'start' | 'center' | 'end' | 'stretch' | 'baseline';
  direction?: 'row' | 'col' | 'row-reverse' | 'col-reverse';
  wrap?: 'wrap' | 'nowrap' | 'wrap-reverse';
}

const Flex = React.forwardRef<HTMLDivElement, FlexProps>(
  ({ className, justify, align, direction, wrap, ...props }, ref) => {
    const justifyClass = justify ? `justify-${justify}` : '';
    const alignItemsClass = align ? `items-${align}` : '';
    const directionClass = direction ? `flex-${direction}` : '';
    const flexWrapClass = wrap ? `flex-${wrap}`: '';

    return (
      <div
        ref={ref}
        className={cn(
          'flex',
          justifyClass,
          alignItemsClass,
          directionClass,
          flexWrapClass,
          className
        )}
        {...props}
      />
    );
  }
);
Flex.displayName = 'Flex';


// Stack Components (VStack and HStack)
export interface StackProps extends FlexProps {
  gap?: keyof typeof spacing;
}

export const VStack = React.forwardRef<HTMLDivElement, StackProps>(
    ({ className, gap = 'md', ...props }, ref) => {
        const gapClass = `gap-${spacing[gap]}`;
        return <Flex ref={ref} direction="col" className={cn(gapClass, className)} {...props} />
    }
)
VStack.displayName = "VStack"

export const HStack = React.forwardRef<HTMLDivElement, StackProps>(
    ({ className, gap = 'md', ...props }, ref) => {
        const gapClass = `gap-${spacing[gap]}`;
        return <Flex ref={ref} direction="row" className={cn(gapClass, className)} {...props} />
    }
)
HStack.displayName = "HStack"


// Safe Area Handling
// This component adds padding to account for mobile browser UI and notches.
// This requires `viewport-fit=cover` in the main HTML file's meta tags.
export interface SafeAreaContainerProps extends React.HTMLAttributes<HTMLDivElement> {}

const SafeAreaContainer = React.forwardRef<HTMLDivElement, SafeAreaContainerProps>(
  ({ className, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(
          'pt-[env(safe-area-inset-top)] pr-[env(safe-area-inset-right)] pb-[env(safe-area-inset-bottom)] pl-[env(safe-area-inset-left)]',
          className
        )}
        {...props}
      />
    );
  }
);
SafeAreaContainer.displayName = 'SafeAreaContainer';


export { Container, Grid, Flex, SafeAreaContainer };
