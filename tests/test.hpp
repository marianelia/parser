#include <iostream>
#include <string>

#pragma once

using namespace std;

bool comparator(long long a, long long b)
{
	return a >= b ? a : b;
}

class TimePoint {
public:
	void SetSeconds(const int new_seconds) { seconds = new_seconds; }

	TimePoint() { seconds = 0; }
	TimePoint(const int new_hours, const int new_minutes, const int new_seconds) {
		TranslateInSeconds(new_hours, new_minutes, new_seconds);
	}

	~TimePoint() {}

	int GetInSeconds() const { return seconds; }

	string Get() const {		
		return TranslateFromSeconds();
	}

private:
	void TranslateInSeconds(int hour, int minute, int second) {
		seconds = hour * 3600 + minute * 60 + second;
	}
	string TranslateFromSeconds() const {
		int hour = seconds / 3600;
		int minute = (seconds % 3600) / 60;
		int second = seconds - hour * 3600 - minute * 60;
		string h = to_string(hour);
		string m = to_string(minute);
		string s = to_string(second);
		string time = "";
		if (hour < 10) { time += '0'; }
		time += h;
		time += ':';
		if (minute < 10) { time += '0'; }
		time += m;
		time += ':';
		if (second < 10) { time += '0'; }
		time += s;
		return time;
	}

	int seconds;
};
