# -*- coding: utf-8 -*-

# Copyright 2012 Jerry Peng
#
# Tomate is a time management tool inspired by the
# pomodoro technique(http://www.pomodorotechnique.com/).
#
# Tomate is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option
# any later version.
#
# Tomate is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public
# License along with Foobar. If not, see http://www.gnu.org/licenses/.


import random


_quote_src = '''
Better three hours too soon, than one minute too late.  --William Shakespeare
Time is the wisest counselor of all.  --Pericles
Time is the school in which we learn, time is the fire in which we burn.  --Delmore Schwartz
Nothing is a waste of time if you use the experience wisely.  --Rodin
Time as he grows old teaches many lessons.  --Aeschylus
Histories make men wise.  --Francis Bacon
Time is what we want most, but what we use worst.  --William Penn
The common man is not concerned about the passage of time, the man of talent is driven by it.  --Shoppenhauer
Time = life; therefore, waste your time and waste of your life, or master your time and master your life.  --Alan Lakein
Don’t be fooled by the calendar. There are only as many days in the year as you make use of. One man gets only a week’s value out of a year while another man gets a full year’s value out of a week.  --Charles Richards
The key is in not spending time, but in investing it.  --Stephen R. Covey
Ordinary people think merely of spending time. Great people think of using it.  --Author Unknown
Determine never to be idle. No person will have occasion to complain of the want of time who never loses any. It is wonderful how much can be done if we are always doing.  --Thomas Jefferson
Make use of time, let not advantage slip.  --William Shakespeare
This time, like all times, is a very good one, if we but know what to do with it.  --Ralph Waldo Emerson
A man who dares to waste one hour of life has not discovered the value of life.  --Charles Darwin
Dost thou love life? Then do not squander time, for that is the stuff life is made of.  --Benjamin Franklin
Once you have mastered time, you will understand how true it is that most people overestimate what they can accomplish in a year – and underestimate what they can achieve in a decade!  --Anthony Robbins
If you want to make good use of your time, you’ve got to know what’s most important and then give it all you’ve got.  --Lee Iacocca
It’s not enough to be busy, so are the ants. The question is, what are we busy about?  --Henry David Thoreau
Take care of the minutes and the hours will take care of themselves.  --Lord Chesterfield
You’re writing the story of your life one moment at a time.  --Doc Childre and Howard Martin
To do two things at once is to do neither.  --Publius Syrus
One cannot manage too many affairs: like pumpkins in the water, one pops up while you try to hold down the other.  --Chinese Proverb
Never let yesterday use up today.  --Richard H. Nelson
I don’t think of the past. The only thing that matters is the everlasting present.  --W. Somerset Maugham
It’s how we spend our time here and now, that really matters. If you are fed up with the way you have come to interact with time, change it.  --Marcia Wieder
Realize that now, in this moment of time, you are creating. You are creating your next moment. That is what’s real.  --Sara Paddison
The time for action is now. It’s never too late to do something.  --Carl Sandburg
You cannot do a kindness too soon, for you never know how soon it will be too late.  --Ralph Waldo Emerson
Whether it’s the best of times or the worst of times, it’s the only time we’ve got.  --Art Buchwald
He lives long that lives well; and time misspent is not lived but lost.  --Thomas Fuller
He who know most grieves most for wasted time.  --Dante
Lost wealth may be replaced by industry, lost knowledge by study, lost health by temperance or medicine, but lost time is gone forever.  --Samuel Smiles
Money, I can only gain or lose. But time I can only lose. So, I must spend it carefully.  --Author Unknown
One thing you can’t recycle is wasted time.  --Author Unknown
Lost time is never found again.  --Proverb
All that really belongs to us is time; even he who has nothing else has that.  --Baltasar Gracian
Time is the most valuable thing a man can spend.  --Theophrastus
Time is money.  --Benjamin Franklin
Gaining time is gaining everything in love, trade and war.  --John Shebbeare
Until you value yourself, you will not value your time. Until you value your time, you will not do anything with it.  --M. Scott Peck
Your greatest resource is your time.  --Brian Tracy
You cannot kill time without injuring eternity.  --Henry David Thoreau
Time is the most valuable thing a man can spend.  --Laertius Diogenes
Time is at once the most valuable and the most perishable of all our possessions.  --John Randolph
Time is really the only capital that any human being has, and the only thing he can’t afford to lose.  --Thomas Edison
Until we can manage time, we can manage nothing else.  --Peter F. Drucker
What may be done at any time will be done at no time.  --Scottish Proverb
A wise person does at once, what a fool does at last. Both do the same thing; only at different times.  --Baltasar Gracian
One worthwhile task carried to a successful conclusion is worth half-a-hundred half-finished tasks.  --Malcolm S. Forbes
To think too long about doing a thing often becomes its undoing.  --Eva Young
A year from now you will wish you had started today.  --Karen Lamb
The surest way to be late is to have plenty of time.  --Leo Kennedy
While we are postponing, life speeds by.  --Seneca
You may delay, but time will not.  --Benjamin Franklin
Never leave ’till tomorrow which you can do today.  --Benjamin Franklin
You will never “find” time for anything. If you want time, you must make it.  --Charles Bruxton
Don’t say you don’t have enough time. You have exactly the same number of hours per day that were given to Helen Keller, Pasteur, Michelangelo, Mother Teresa, Leonardo da Vinci, Thomas Jefferson, and Albert Einstein.  --H. Jackson Brown
The bad news is time flies. The good news is you’re the pilot.  --Michael Altshuler
Time is the coin of your life. It is the only coin you have, and only you can determine how it will be spent. Be careful lest you let other people spend it for you.  --Carl Sandburg
I am definitely going to take a course on time management… just as soon as I can work it into my schedule.  --Louis E. Boone
In truth, people can generally make time for what they choose to do; it is not really the time but the will that is lacking.  --Sir John Lubbock
Those who make the worse use of their time are the first to complain of its shortness.  --Jean De La Bruyere
The great dividing line between success and failure can be expressed in five words: “I did not have time.”  --Franklin Field
'''

def _parse_quotes():
    quotes = []
    for l in _quote_src.splitlines():
        if not l:
            continue
        p = l.find('--')
        if p > 0:
            quotes.append((l[:p].strip(), l[p+2:].strip()))
        else:
            quotes.append((l.strip(), 'Author Unknown'))
    return tuple(quotes)

_quotes = _parse_quotes()

def random_quote():
    return random.choice(_quotes)

if __name__ == '__main__':
    print random_quote()
