import * as React from 'react';

const cn = (...classes: (string | undefined | null | false)[]) => {
  return classes.filter(Boolean).join(' ');
};

export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'secondary' | 'destructive' | 'success';
}

const Badge = React.forwardRef<HTMLDivElement, BadgeProps>(
  ({ className, variant = 'default', ...props }, ref) => {
    const baseClasses =
      'inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2';

    const variantClasses = {
      default: 'border-transparent bg-blue-600 text-white',
      secondary: 'border-transparent bg-gray-200 text-gray-800',
      destructive: 'border-transparent bg-red-600 text-white',
      success: 'border-transparent bg-green-600 text-white',
    };

    const finalClasses = cn(
      baseClasses,
      variantClasses[variant],
      className
    );

    return (
      <div
        className={finalClasses}
        ref={ref}
        {...props}
      />
    );
  }
);
Badge.displayName = 'Badge';

export { Badge };
