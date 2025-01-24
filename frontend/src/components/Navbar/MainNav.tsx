import { FC } from 'react';
import Link from 'next/link';
import { Rocket } from 'lucide-react';
import {
    NavigationMenu,
    NavigationMenuItem,
    NavigationMenuLink,
    NavigationMenuList,
    navigationMenuTriggerStyle,
} from '@/components';
import { navItems } from '@/lib';

export const MainNav: FC = () => {
    return (
        <div className="mr-4 hidden md:flex items-center space-x-6">
            <Link href="/" className="flex items-center space-x-2">
                <Rocket className="h-6 w-6" />
                <span className="hidden font-bold sm:inline-block">Acme Inc</span>
            </Link>
            <NavigationMenu>
                <NavigationMenuList className="flex space-x-4">
                    {navItems.map((item) => (
                        <NavigationMenuItem key={item.title}>
                            <NavigationMenuLink
                                className={navigationMenuTriggerStyle()}
                                href={item.href}
                            >
                                {item.title}
                            </NavigationMenuLink>
                        </NavigationMenuItem>
                    ))}
                </NavigationMenuList>
            </NavigationMenu>
        </div>
    );
};
