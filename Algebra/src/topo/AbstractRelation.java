package topo;

public abstract class AbstractRelation<E extends Element<E>,A extends AbstractRelation<E,A>> implements TopoSpace<A,PairedElement<E>>, Relation<E,A>{
	protected PairedElement<E> basePoint;
	public AbstractRelation() {}
	public PairedElement<E> basePoint(){return basePoint==null?null:basePoint;}
	public A complement(){
		A inv = inverse();
		
		return inv!=null?inv:null;
	}
	public boolean contains(PairedElement<E> element){
		if(basePoint==null){
			if(isRelated(element.getFirst(),element.getSecond())) basePoint = new PairedElement<E> (element);
		}
		return isRelated(element.getFirst(),element.getSecond());
	}
	public boolean equals(Object o){
		if(this==o) return true;
		if(!(o instanceof AbstractRelation)) return false;
		AbstractRelation<?,?> cp = (AbstractRelation<?,?>) o;
		if(basePoint==null&&cp.basePoint==null) return true;
		if(basePoint!=null&&cp.basePoint!=null){
			if(basePoint.getElementClass().equals(cp.basePoint.getElementClass())){
				@SuppressWarnings("unchecked")
				A cp1 = (A) cp;
				return isSuperSet(cp1)&&isSubSet(cp1);
			}
		}
		return false;
	}
	@SuppressWarnings("unchecked")
	public A intersect(A another){
		final AbstractRelation<E,A> firstRel = this;
		final AbstractRelation<E,A> secondRel= another;
		AbstractRelation<E,A>inter = new AbstractRelation<E,A> (){
			public boolean isClosed() {
				// TODO Auto-generated method stub
				return firstRel.isClosed()&&secondRel.isClosed();
			}

			public boolean isEmpty(){return firstRel.isEmpty()||secondRel.isEmpty();}
			
			public boolean isRelated(E first, E second) {
				if(basePoint==null) basePoint = new PairedElement<E>(first,second);
				return firstRel.isRelated(first, second)&&secondRel.isRelated(first, second);
			}

			
			public boolean isOpen() {return firstRel.isOpen()&&secondRel.isOpen();}
			
		};
		return (A) inter;
	}
	
	@SuppressWarnings("unchecked")
	public A inverse(){
		final AbstractRelation<E,A> rel = this;
		return (A) new AbstractRelation<E,A> (){

			//basePoint = new PairedElement<E>(rel.basePoint());
			public boolean isClosed() {return !rel.isClosed();}

			
			public boolean isRelated(E first, E second) {
				if(basePoint==null){
					if(!rel.isRelated(first, second)) {
						basePoint = new PairedElement<E>(first,second);
						return true;
					}
					return false;
				}	
				return !rel.isRelated(first, second);
			}

			
			public boolean isEmpty() {return rel.isClosed()&&rel.isOpen()&&rel.basePoint!=null?true:false;}

			
			public boolean isOpen() {return rel.isClosed();}
			
		};
	}
	//public boolean isEmpty(){return false;}
	//public boolean isOpen(){return false;}
	public boolean isSubSet (A another){
		return intersect(another).equals(this);
	}
	public boolean isSuperSet (A another){
		return intersect(another).equals(another);
	}
	
	@SuppressWarnings("unchecked")
	public A union (A another){
		final AbstractRelation<E,A> rel1 = this, rel2 = another;
		return (A) new AbstractRelation<E,A> (){
			
			public boolean isClosed() {return rel1.isClosed()&&rel2.isClosed();}

			
			public boolean isRelated(E first, E second) {
				if(basePoint==null){
					if(rel1.isRelated(first, second)||rel2.isRelated(first, second)) {
						basePoint = new PairedElement<E>(first,second);
						return true;
					}
					return false;
				}
				return rel1.isRelated(first, second)||rel2.isRelated(first, second);
			}

			
			public boolean isEmpty() {return rel1.isEmpty()||rel2.isEmpty();}

			
			public boolean isOpen() {return rel1.isOpen()&&rel2.isOpen();}
			
		};
	}
	
	
}
