package util;

public class IntPair implements Comparable<IntPair>{
	private int  first;
	private int second;
	public IntPair(int first, int second){
		this.first = first;
		this.second = second;
	}
	public boolean equals (Object o){
		if(!(o instanceof IntPair)) return false;
		IntPair cp = (IntPair) o;
		return first==cp.first&&second==cp.second?true:false;
	}
	public int compareTo(IntPair o) {
		if(first<o.first) return -1;
		if(first>o.first) return 1;
		return second<o.second?-1:second>o.second?1:0;
	}
	public int getFirst (){return first;}
	public int getSecond (){return second;}
}
