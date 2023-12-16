So the exhaustive search was taking too long. SO instead I skipped through the ranges, initially jumping
16,384, then 8,192, etc. This came up with answers but they were wrong. SO, instead, I looked at the last best location
+/- 32768 and then only skipped through starting at 1,024, 512, etc. This yielded the correct answer.

My logic was that while the multiple steps made it impossible to predict where each seed would land, I saw that
whole ranges of values resulted in the same location slowly increasing. That implied there was a good correlation
between the source seeds and the final locations. Whenever a range split happened, there would obviously be a jump
in location (maybe up, maybe down), it meant it wasn't totally random (like an encrypted)








Seeds 79-92, 55-67

seed to soil 
  D:50-51, S:98-99
  D: 52-99, S:50-97

seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
