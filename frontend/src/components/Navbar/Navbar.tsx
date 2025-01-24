'use client';
import { FC, useEffect } from 'react';
import Link from 'next/link';
import { useUser } from '@auth0/nextjs-auth0/client';
import { Button, MainNav, MobileNav } from '@/components';

export const Navbar: FC = () => {
    const { user, error, isLoading } = useUser();

    console.log(user);

    useEffect(() => {
        if (user) {
            fetch('/api/test')
                .then((response) => response.json())
                .then((data) => console.log(data))
                .catch((error) => console.error('Error fetching data:', error));
        }
    }, [user]);

    return (
        <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
            <div className="container flex h-14 items-center justify-between">
                <MainNav />
                <MobileNav />
                {user ? (
                    <div className="flex items-center space-x-2">
                        <nav className="hidden md:flex items-center space-x-1">
                            <Button asChild variant="ghost">
                                <a href="/api/auth/logout">Dashboard</a>
                            </Button>
                        </nav>
                        <nav className="flex items-center space-x-1 md:hidden">
                            <Button asChild variant="ghost">
                                <a href="/api/auth/login">Dashboard</a>
                            </Button>
                        </nav>
                    </div>
                ) : (
                    <div className="flex items-center space-x-2">
                        <nav className="hidden md:flex items-center space-x-1">
                            <Button asChild variant="ghost">
                                <a href="/api/auth/login">Get Started</a>
                            </Button>
                        </nav>
                        <nav className="flex items-center space-x-1 md:hidden">
                            <Button asChild variant="ghost">
                                <a href="/api/auth/logout">Get Started</a>
                            </Button>
                        </nav>
                    </div>
                )}
            </div>
        </header>
    );
};
