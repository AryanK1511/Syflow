import type { Metadata } from 'next';
import { UserProvider } from '@auth0/nextjs-auth0/client';
import './globals.css';

export const metadata: Metadata = {
    title: 'Syflow',
    description:
        'Provision and customize Minecraft servers on the cloud or your own machine, with real-time logs and effortless management',
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en">
            <UserProvider>
                <body>{children}</body>
            </UserProvider>
        </html>
    );
}
