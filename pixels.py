import pygame
from time import sleep
from random import random

class Sorter:
	def __init__(self):
		pass

	def sort(self,image):
		return image
		


class repeat(Sorter):
	repeats=0
	sorter=None
	def __init__(self,repeats,sorter):
		self.sorter=sorter
		self.repeats=repeats

	def sort(self,image):
		for n in range(self.repeats):
			print ">> repeat %s"%(n)
			image=self.sorter.sort(image)
		return image

class Chain(Sorter):
	sorters=[]
	def __init__(self, *sorters):
		self.sorters=sorters

	def sort(self,image):
		for i in range(len(self.sorters)):
			print "> sorter %s"%(i)
			image=self.sorters[i].sort(image)
		return image

class rotate(Sorter):
	def __init__(self,turns):
		self.turns=turns

	def sort(self,image):
		return pygame.transform.rotate(image,90*self.turns)









class RelayScrambler(Sorter):
	def __init__(self, overwrite=True):
		self.overwrite=overwrite

	def sort(self,image):
		copysurf = image.copy()
		for channel in [0,1,2]:
			print "channel %s"%(channel)
			for x in range(image.get_width()):
				for y in range(image.get_height()):
					ay = int( y+image.get_at( (x,y) ).cmy[channel]*image.get_height() )%image.get_height()
					
					c = image.get_at((x,y))
					b = image.get_at((x,ay))
					if(self.overwrite):
						if(channel==0):
							b.r = c.r
						if(channel==1):
							b.g = c.g
						if(channel==2):
							b.b = c.b
					else:
						if(channel==0):
							n = b.r+c.r
							if(n>255):
								n=255
							b.r=n
						if(channel==1):
							n = b.g+c.g
							if(n>255):
								n=255
							b.g=n
						if(channel==2):
							n = b.b+c.b
							if(n>255):
								n=255
							b.b=n
					copysurf.set_at( (x,ay), b) 

		return copysurf











class MeltIntoWall_broken_1(Sorter):

	def isWall(self,color):
		return color.hsva[2]<10

	def isLarger(self,colorA,colorB):
		return colorA.hsva[2]>colorB.hsva[2]

	def qsort(self,list):
	    if list == []: 
	        return []
	    else:
	        pivot = list[0]
	        lesser = self.qsort([x for x in list[1:] if self.isLarger(pivot,x)])
	        greater = self.qsort([x for x in list[1:] if (x == pivot or self.isLarger(x,pivot))])
	        return lesser + [pivot] + greater


	def sort(self,image):
		out = image.copy();
		for x in range(image.get_width()):
			regionstart=0
			for y in range(image.get_height()):
				if(self.isWall(image.get_at( (x,y) )) or y==image.get_height()-1):
					order = range(regionstart,y)
					#b = order
					for i in range(len(order)):
						order[i]=image.get_at( (x,i) )
					self.qsort(order)
					#print (b,order)

					for i in range(len(order)):
						out.set_at( (x,regionstart+i), order[i] )

					regionstart=y
		return out

class MeltIntoWall_broken_2(Sorter):

	def isWall(self,color):
		return color.hsva[2]<10

	def isLarger(self,colorA,colorB):
		return colorA.hsva[2]>colorB.hsva[2]

	def qsort(self,list):
	    if list == []: 
	        return []
	    else:
	        pivot = list[0]
	        lesser = self.qsort([x for x in list[1:] if self.isLarger(pivot,x)])
	        greater = self.qsort([x for x in list[1:] if (x == pivot or self.isLarger(x,pivot))])
	        return lesser + [pivot] + greater


	def sort(self,image):
		out = image.copy();
		for x in range(image.get_width()):
			regionstart=0
			for y in range(image.get_height()):
				if(self.isWall(image.get_at( (x,y) )) or y==image.get_height()-1):
					order = range(regionstart,y)
					#b = order
					for i in range(len(order)):
						order[i]=image.get_at( (x,order[i]) )
					order=self.qsort(order)
					#print (b,order)

					for i in range(len(order)):
						out.set_at( (x,regionstart+i), order[i] )

					regionstart=y
		return out
















class MeltIntoWall(Sorter):

	def isWall(self,color):
		return color.hsva[2]<=10

	def isLarger(self,colorA,colorB):
		return colorA.hsva[2]>colorB.hsva[2]

	def sort(self,image):
		out = image.copy();
		for x in range(image.get_width()):
			regionstart=0
			for y in range(image.get_height()):
				if(self.isWall(image.get_at( (x,y) )) or y==image.get_height()-1):
					order = range(regionstart,y)
					for i in range(len(order)):
						order[i]=image.get_at( (x,order[i]) )

					order.sort(key = lambda x: x.hsva[2])
					#print (image.get_height(), len(order));

					for i in range(len(order)):
						out.set_at( (x,regionstart+i), order[i] )

					regionstart=y
		return out


class MeltByEh(MeltIntoWall):

	def isWall(self,color):
		return color.hsva[0]%10==0

	def isLarger(self,colorA,colorB):
		return colorA.hsva[1]>colorb.hsva[1]

class Melt(MeltIntoWall):

	def isWall(self,color):
		return False

	def isLarger(self,colorA,colorB):
		return colorA.hsva[1]>colorb.hsva[1]















class bitshift(Sorter):
	shift=0
	def __init__(self, shift):
		self.shift=shift

	def sort(self,image):
		buff = image.get_buffer().raw
		n=len(buff)
		new=""
		for b in range(n):
			if(1.0*b/n)%0.1==0:
				print(1.0*b/n)
			#TODO wraparound for better fx
			if(self.shift>0):
				new+=chr( abs( ord(buff[b])>>self.shift )%256 )
			else:
				new+=chr( abs( ord(buff[b])<< (-self.shift) )%256 )
			

		return pygame.image.fromstring(new,(image.get_width(), image.get_height()), "RGB", False)


class oradjacent(Sorter):
	shift=1
	def __init__(self,shift=1):
		self.shift=shift

	def sort(self,image):
		buff = image.get_buffer().raw
		n=len(buff)
		new=""
		for b in range(n):
			if(1.0*b/n)%0.1==0:
				print(1.0*b/n)
			new+=chr( ( ord(buff[b])|ord(buff[(b+self.shift)%len(buff)]) )%256 )
			

		return pygame.image.fromstring(new,(image.get_width(), image.get_height()), "RGB", False)

class xoradjacent(Sorter):
	def __init__(self,shift=1):
		self.shift=shift

	def sort(self,image):
		buff = image.get_buffer().raw
		n=len(buff)
		new=""
		for b in range(n):
			if(1.0*b/n)%0.1==0:
				print(1.0*b/n)
			new+=chr( ( ord(buff[b])^ord(buff[(b+self.shift)%len(buff)]) )%256 )
			

		return pygame.image.fromstring(new,(image.get_width(), image.get_height()), "RGB", False)

class andadjacent(Sorter):
	def __init__(self,shift=1):
		self.shift=shift

	def sort(self,image):
		buff = image.get_buffer().raw
		n=len(buff)
		new=""
		for b in range(n):
			if(1.0*b/n)%0.1==0:
				print(1.0*b/n)
			new+=chr( ( ord(buff[b])&ord(buff[(b+self.shift)%len(buff)]) )%256 )
			

		return pygame.image.fromstring(new,(image.get_width(), image.get_height()), "RGB", False)

class sortbycolumn(Sorter):
	columnwidth=0
	def __init__(self,columnwidth=0):
		self.columnwidth=columnwidth

	def evaluate(self,img):
		value = 0
		for x in range(img.get_width()):
			for y in range(img.get_height()):
				value+=self.ecol(img.get_at( (x,y) ))
		return value

	def ecol(self,color):
		return color.hsva[1]

	def sort(self,image):
		out = image.copy()
		blocks = []
		for i in range(image.get_width()/self.columnwidth):
			img = pygame.Surface( (self.columnwidth, image.get_height()) )
			img.blit(image, (-i*self.columnwidth,0) )
			blocks.append( img )
		if ( image.get_width()%self.columnwidth!=0 ):
			xoff = (image.get_width()/self.columnwidth)*self.columnwidth#because rounding
			i = pygame.Surface((
				image.get_width()-xoff,
				image.get_height() ))
			i.blit(image, (-xoff,0) )
			blocks.append(i)

		for i in range(len(blocks)):
			blocks[i] = (self.evaluate(blocks[i]),blocks[i])

		blocks.sort(key = lambda x: x[0])

		x=0
		for i in blocks:
			out.blit(i[1],(x,0))
			x+=i[1].get_width()

		return out

class sortbycolumn_hue(sortbycolumn):
	def ecol(self,color):
		return color.hsva[0]

class sortbycolumn_r(sortbycolumn):
	def ecol(self,color):
		return color.r

class transposebits(Sorter):

	def __init__(self, start, length, insert=1.0):
		self.startpoint = start #startpoint as a fraction
		self.length=length	#length as a fraction
		self.insert=insert

	def sort(self,image):
		buff = image.get_buffer().raw
		n=len(buff)
		start = int(n*self.startpoint)
		end = int(n*self.startpoint+n*self.length)

		new = buff[0:start]+buff[start:end]
		ins=buff[start:end]
		
		inspoint = int( n*self.insert )
		new = new[0:inspoint]+ins+new[inspoint:]

		return pygame.image.fromstring(new,(image.get_width(), image.get_height()), "RGB", False)

class randomtransposition(transposebits):
	def __init__(self):
		transposebits.__init__(self,random(),random(),random())

















def main():
	pygame.init()

	print "working"

	#sorter = Chain( sortbycolumn(1) )
	#sorter = Chain( oradjacent(), rotate(1), sortbycolumn(20), rotate(-1) )
	#sorter = Chain( andadjacent(), rotate(1), sortbycolumn(20), rotate(-1), sortbycolumn(20))
	#sorter = Chain( sortbycolumn(5), rotate(-1), sortbycolumn(5), rotate(1) )
	#sorter = Chain( Melt(), rotate(1), Melt(), rotate(-1) )
	#sorter = Chain( rotate(1), sortbycolumn(10), rotate(-1), MeltByEh() )
	#sorter = Chain( rotate(1), sortbycolumn(10), rotate(-1), RelayScrambler(), MeltByEh() )
	#sorter = Chain( rotate(1), sortbycolumn(10), rotate(-1), xoradjacent(), MeltByEh() )
	#sorter = Chain(rotate(-1), MeltByEh(), rotate(3), sortbycolumn(10) )
	#sorter = Chain(rotate(-1), sortbycolumn(20), rotate(1))
	#sorter = Chain(sortbycolumn(20))
	
	#sorter = transposebits(0.2,0.2,0.3)
	#sorter = repeat( 10, randomtransposition() )
	sorter = Chain( repeat( 10, randomtransposition() ), rotate(1), sortbycolumn(10), rotate(3) )


	raw = pygame.image.load("test.jpg")
	out = sorter.sort( raw )
	print "done"
	joined = pygame.Surface( (raw.get_width()*2, raw.get_height()) )
	joined.blit(raw, (0,0));
	joined.blit(out, (raw.get_width(),0))
	pygame.image.save(joined,"test_pair.jpg")
	pygame.image.save(out,"test_out.jpg")

	screen = pygame.display.set_mode((joined.get_width(), joined.get_height()))
	running=True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running=False
		sleep(1.0/60)
		screen.blit(joined,(0,0) )
		pygame.display.flip()

main()

