# A call to this program will be of the form '' python Plot [Exact] [totalE] [Output] ''
# Exact  [0 = plot only solver solution, 1 = plot exact solution]
# totalE [0 = plot only internal energy, 1 = plot total energy]
# Output [0 = create .png files        , 1 = create animation pop up  , 2 = create .mp4 file]
height = 12         # Height of plot in inches (12 is good for a video)
width  = 15         # Width  of plot in inches
floor  = [-3000.,3000.] # Limits on plotting axes
pad    = 3

import os
import sys
from matplotlib import pyplot as plt
from matplotlib import animation


Exact  = sys.argv[1]
totalE = sys.argv[2]
Output = sys.argv[3]
#
# Exact  = '1'
# totalE = '0'
# Output = '1'


def ReadInData(file):
	content = []
	file = open(file,'r')
	file = file.read().splitlines()
	for line in file:
		line = line.split(' ')
		row  = [float(item) for item in line if item != '']
		content.append(row)
	return content

def limitFinder(array,frac):
	mini = min([min(element) for element in array])
	maxi = max([max(element) for element in array])
	mini -= frac*abs(mini)
	maxi += frac*abs(maxi)
	limits = [max(floor[0],mini),min(floor[1],maxi)]
	return limits

def Plot_set_single(ax1,i=0):
	ax1.set_xlabel('r',fontsize=20),ax1.set_ylabel(r'$\rho$',fontsize=20)
	plt.suptitle(' Time %f  ' %( t[i][0] ))
	ax1.set_xlim(x_lim)  , ax1.set_ylim(e_lim) , ax1.grid()
	return

def Plot_set(ax1,ax2,ax3,ax4,ax5=0,i=0):
	ax1.set_xlabel('r'),ax1.set_ylabel(r'$\rho$')
	ax2.set_xlabel('r'),ax2.set_ylabel('u')
	ax3.set_xlabel('r'),ax3.set_ylabel('P')
	ax4.set_xlabel('r'),ax4.set_ylabel('e')
	plt.suptitle(' Step %i Time %f , Total Mass %f ' %( int(step[i][0]) , t[i][0] , mass[i][0]))
	ax1.set_xlim(x_lim)   , ax2.set_xlim(x_lim)
	ax3.set_xlim(x_lim)   , ax4.set_xlim(x_lim)
	ax1.set_ylim(rho_lim) , ax2.set_ylim(u_lim)
	ax3.set_ylim(P_lim)   , ax4.set_ylim(e_lim)
	ax1.grid()            ,ax2.grid()
	ax3.grid()            ,ax4.grid()
	if totalE=='1':
		ax5.set_xlabel('r'),ax5.set_ylabel('E')
		ax5.set_xlim(x_lim),ax5.set_ylim(eT_lim)
		ax5.grid()
	return

def SavePng(plt,ax1,ax2,ax3,ax4,j,ax5=0):
	if j < 10:
		plt.savefig('Output/Pictures/Image'+pad*'0'+'%i.png' % j)
	elif j >= 10 and j < 100:
		plt.savefig('Output/Pictures/Image'+(pad-1)*'0'+'%i.png' % j)
	elif j >= 100 and j < 1000:
		plt.savefig('Output/Pictures/Image'+(pad-2)*'0'+'%i.png' % j)
	elif j >= 1000 and j < 10000:
		plt.savefig('Output/Pictures/Image'+(pad-3)*'0'+'%i.png' % j)
	else :
		print('Must ammed padding for more images')
	ax1.cla(),ax2.cla(),ax3.cla(),ax4.cla()
	if totalE=='1':
		ax5.cla()
	return
def SavePng_single(plt,ax1,j):
	if j < 10:
		plt.savefig('Output/Pictures/Image'+pad*'0'+'%i.png' % j)
	elif j >= 10 and j < 100:
		plt.savefig('Output/Pictures/Image'+(pad-1)*'0'+'%i.png' % j)
	elif j >= 100 and j < 1000:
		plt.savefig('Output/Pictures/Image'+(pad-2)*'0'+'%i.png' % j)
	elif j >= 1000 and j < 10000:
		plt.savefig('Output/Pictures/Image'+(pad-3)*'0'+'%i.png' % j)
	else :
		print('Must added more index padding for more images')
	ax1.cla()
	return
# Read in the data
if Exact=='1':
	file_name_e	= sorted([ 'Exact/Output/'+fn for fn in os.listdir(os.getcwd()+'/Exact/Output') if fn.endswith('.txt')],key=str.lower)
	energy_e     = ReadInData(file_name_e[0])		# Exact internal energy
	r_e          = ReadInData(file_name_e[1])[0]   # Exact positions
	press_e      = ReadInData(file_name_e[2])		# Exact pressure
	rho_e	     = ReadInData(file_name_e[3])		# Exact rho
	vel_e	     = ReadInData(file_name_e[4])		# Exact velocity

file_name_m	= sorted([ 'Output/'+fn for fn in os.listdir(os.getcwd()+'/Output') if fn.endswith('.txt')],key=str.lower)
t         = ReadInData(file_name_m[0])	     # CurrentTime
rho       = ReadInData(file_name_m[1])       # Density
states    = ReadInData(file_name_m[2])       # Intial states (only used for exact fortran code)
energy    = ReadInData(file_name_m[3])       # Internal Energy
lrc       = ReadInData(file_name_m[4])       # Lagrange cell center
lre       = ReadInData(file_name_m[5])       # Lagrange cell edges
press     = ReadInData(file_name_m[6]) 	     # Pressure
step      = ReadInData(file_name_m[7])       # Step number
energyT   = ReadInData(file_name_m[8])       # Total energy
mass      = ReadInData(file_name_m[9])       # Total mass
vel       = ReadInData(file_name_m[10])	     # Velocity

# Determine plotting limits
# x_lim   = [0.4,1.0]
# rho_lim = [0.,4.4]
x_lim   = limitFinder(lrc,0.)
rho_lim = limitFinder(rho,.1)
u_lim   = limitFinder(vel,.1)
P_lim   = limitFinder(press,.1)
e_lim   = limitFinder(energy,.1)
eT_lim  = limitFinder(energyT,.1)


# Create figure to plot to
if Output!='3':
	fig = plt.figure(1)
	fig.set_size_inches(width,height, True)
	ax1 = fig.add_subplot(2,2+int(totalE),1)
	ax2 = fig.add_subplot(2,2+int(totalE),2)
	ax3 = fig.add_subplot(2,2+int(totalE),3)
	ax4 = fig.add_subplot(2,2+int(totalE),4)
	if totalE=='1':
		ax5 = fig.add_subplot(2,3,5)
		ax5.grid()
else:
	fig = plt.figure(1)
	fig.set_size_inches(width,height, True)
	ax1 = fig.add_subplot(111)

# Create images
if Output == '0':
	for i in range(len(rho)):
		# Create scatter plot and line plot objects
		Plot_set(ax1,ax2,ax3,ax4,i=i)
		ax1.scatter(lrc[i],rho[i],facecolors='none',edgecolors='k')
		ax2.scatter(lrc[i],vel[i],facecolors='none',edgecolors='k')
		ax3.scatter(lrc[i],press[i],facecolors='none',edgecolors='k')
		ax4.scatter(lrc[i],energy[i],facecolors='none',edgecolors='k')
		if Exact=='1':   # Plot the exact solution
			ax1.plot(r_e,rho_e[i])
			ax2.plot(r_e,vel_e[i])
			ax3.plot(r_e,press_e[i])
			ax4.plot(r_e,energy_e[i])
			if totalE== '1':
				ax5.scatter(lrc[i],energyT[i],facecolors='none',edgecolors='k')
		j = int(i+1)
		SavePng(plt,ax1,ax2,ax3,ax4,j)

if Output == '3':
	for i in range(len(rho)):
		# Create scatter plot and line plot objects
		Plot_set_single(ax1,i=i)
		sol = ax1.scatter(lrc[i],energy[i],facecolors='none',edgecolors='k',label='PPM')
		if Exact=='1':   # Plot the exact solution
			exact,=ax1.plot(r_e,energy_e[i],label='Exact')
		j = int(i+1)
		SavePng_single(plt,ax1,j)

# Create video of animation
if Output == '1' or Output == '2':
		# Create intial figure
		Plot_set(ax1,ax2,ax3,ax4,i=0)
		scat1 = ax1.scatter(lrc[0],rho[0],facecolors='none',edgecolors='k')
		scat2 = ax2.scatter(lrc[0],vel[0],facecolors='none',edgecolors='k')
		scat3 = ax3.scatter(lrc[0],press[0],facecolors='none',edgecolors='k')
		scat4 = ax4.scatter(lrc[0],energy[0],facecolors='none',edgecolors='k')
		if Exact=='1' :   # Plot the exact solution
			plt1, = ax1.plot(r_e,rho_e[0])
			plt2, = ax2.plot(r_e,vel_e[0])
			plt3, = ax3.plot(r_e,press_e[0])
			plt4, = ax4.plot(r_e,energy_e[0])
		if totalE=='1':
			scat5 = ax5.scatter(lrc[0],energyT[0],facecolors='none',edgecolors='k')
		else :
			scat5,ax5 = 0.,0.


		def updateExact(i,fig,scat1,scat2,scat3,scat4,plt1,plt2,plt3,plt4,scat5):
			plt1.set_data(r_e,rho_e[i])
			plt2.set_data(r_e,vel_e[i])
			plt3.set_data(r_e,press_e[i])
			plt4.set_data(r_e,energy_e[i])
			scat1.set_offsets([[lrc[i][j],rho[i][j]]    for j in range(len(rho[i])-1)])
			scat2.set_offsets([[lrc[i][j],vel[i][j]]    for j in range(len(vel[i])-1)])
			scat3.set_offsets([[lrc[i][j],press[i][j]]  for j in range(len(press[i])-1)])
			scat4.set_offsets([[lrc[i][j],energy[i][j]] for j in range(len(energy[i])-1)])
			if totalE=='1':
				scat5.set_offsets([[lrc[i][j],energyT[i][j]] for j in range(len(energyT[i])-1)])
			plt.suptitle(' Step %i Time %f , Total Mass %f ' %( int(step[i][0]) , t[i][0] , mass[i][0]))
			Plot_set(ax1,ax2,ax3,ax4,ax5,i=i)
			return scat1,scat2,scat3,scat4

		def updateSolution(i,fig,scat1,scat2,scat3,scat4,scat5):
			scat1.set_offsets([[lrc[i][j],rho[i][j]]    for j in range(len(rho[i])-1)])
			scat2.set_offsets([[lrc[i][j],vel[i][j]]    for j in range(len(vel[i])-1)])
			scat3.set_offsets([[lrc[i][j],press[i][j]]  for j in range(len(press[i])-1)])
			scat4.set_offsets([[lrc[i][j],energy[i][j]] for j in range(len(energy[i])-1)])
			if totalE=='1':
				scat5.set_offsets([[lrc[i][j],energyT[i][j]] for j in range(len(energyT[i])-1)])
			plt.suptitle(' Step %i Time %f , Total Mass %f ' %( int(step[i][0]) , t[i][0] , mass[i][0]))
			Plot_set(ax1,ax2,ax3,ax4,ax5,i=i)
			return scat1,scat2,scat3,scat4

		if Exact == '1':
			anim = animation.FuncAnimation(fig, updateExact,fargs=(fig,scat1,scat2,scat3,scat4,plt1,plt2,plt3,plt4,scat5),frames=len(rho),interval=500)
		else:
			anim = animation.FuncAnimation(fig, updateSolution,fargs=(fig,scat1,scat2,scat3,scat4,scat5),frames=len(rho),interval=500)

		if Output == '1':
			plt.show()
		elif Output == '2':
			anim.save('Output/out.mp4', fps=2)
