'use client';

import { FC } from 'react';
import { Menu, Rocket } from 'lucide-react';
import { Sheet, SheetTrigger, Button, SheetContent, MobileLink } from '@/components';
import { navItems } from '@/lib';

export const MobileNav: FC = () => {
    return (
        <Sheet>
            <SheetTrigger asChild>
                <Button
                    variant="ghost"
                    className="mr-2 px-0 text-base hover:bg-transparent focus-visible:bg-transparent focus-visible:ring-0 focus-visible:ring-offset-0 md:hidden"
                >
                    <Menu className="h-5 w-5" />
                    <span className="sr-only">Toggle Menu</span>
                </Button>
            </SheetTrigger>
            <SheetContent side="left" className="pr-0">
                <MobileLink href="/" className="flex items-center" onOpenChange={() => {}}>
                    <Rocket className="mr-2 h-4 w-4" />
                    <span className="font-bold">Acme Inc</span>
                </MobileLink>
                <div className="my-4 h-[calc(100vh-8rem)] pb-10 pl-6">
                    <div className="flex flex-col space-y-3">
                        {navItems.map((item) => (
                            <MobileLink key={item.href} href={item.href} onOpenChange={() => {}}>
                                {item.title}
                            </MobileLink>
                        ))}
                    </div>
                </div>
                <div className="border-t pt-4">
                    <MobileLink href="/sign-in" onOpenChange={() => {}}>
                        Sign In
                    </MobileLink>
                </div>
            </SheetContent>
        </Sheet>
    );
};
