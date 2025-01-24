import { FC } from 'react';
import Link from 'next/link';
import { cn } from '@/lib';

interface MobileLinkProps extends React.ComponentPropsWithoutRef<'a'> {
    onOpenChange?: (open: boolean) => void;
    children: React.ReactNode;
    href: string;
}

export const MobileLink: FC<MobileLinkProps> = ({
    href,
    onOpenChange,
    className,
    children,
    ...props
}) => {
    return (
        <Link
            href={href}
            onClick={() => {
                onOpenChange?.(false);
            }}
            className={cn(className)}
            {...props}
        >
            {children}
        </Link>
    );
};
