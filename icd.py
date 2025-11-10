import matplotlib.pyplot as plt
import numpy as np
import scipy.stats

from scipy.optimize import curve_fit

def poisson_f(x, k, λ):
    return k * scipy.stats.poisson.pmf(x, λ)

def angle_distribution(x, norm, n):
    return norm * np.abs(np.cos(np.deg2rad(x)))**n

np.random.seed(12346765)

def latex_float(f):
    float_str = "{0:.2g}".format(f)
    if "e" in float_str:
        base, exponent = float_str.split("e")
        return r"{0} \times 10^{{{1}}}".format(base, int(exponent))
    else:
        return float_str

class ICD:
    def __init__(self, fake=False):
        print('---------------------------------------------')
        print('   International cosmic day @ INFN Genova    ')
        print('---------------------------------------------')
        print('                interactive                  ')
        print()
        self.__routine__(fake)

    def __plot_init_routine__(self):
        self.figure, self.ax = plt.subplots()
        self.ax.text(.025, .95, 'International Cosmic Day @ INFN Genova',
                     transform=self.ax.transAxes, fontproperties={'weight': 'bold'})

    def __routine__(self, fake):
        pass


class hist(ICD):

    def __load_data__(self):
        self.nmin = int(input('Dimmi il valore minimo '))
        self.nmax = int(input('Dimmi il valore massimo '))

        self.nbins = self.nmax - self.nmin + 1
        data = []
        area = 0

        print('Ora raccogliamo i dati!')

        for i in range(self.nbins):
            nmeasures = int(input(f'Dimmi quante volte hai misurato {self.nmin + i} : '))
            area += nmeasures
            for _ in range(nmeasures):
                data.append(self.nmin + i)

        print(f'Area totale misurata {area}')

        self.hist = np.histogram(data, bins=self.nbins, range=(self.nmin-0.5, self.nmax+0.5),
                                 density=False)
        self.data = np.array(data)

    def Plot(self):
        self.__plot_init_routine__()
        self.mode = 'plot'

        counts, bin_edges = self.hist
        bin_centers = 0.5*(bin_edges[1:] + bin_edges[:-1])

        counts_error = np.sqrt(counts)
        area = np.sum(counts)
        norm_counts = counts / area
        norm_counts_error = counts_error / area
        bin_width = bin_edges[1] - bin_edges[0]

        self.ax.errorbar(bin_centers, norm_counts, norm_counts_error, xerr=bin_width/2,
                         marker='o', ms=3, ls='', color='k', label='Dati sperimentali')

        self.ax.text(1-.025, .8, f'Eventi totali {area}', transform=self.ax.transAxes, ha='right')
        self.ax.set_ylabel('Frequenza')
        self.ax.set_ylim(0, 0.25)

    def Fit(self):
        self.mode = 'fit'

        counts, bin_edges = self.hist
        bin_centers = 0.5*(bin_edges[1:] + bin_edges[:-1])

        counts_error = np.sqrt(counts)
        area = np.sum(counts)
        norm_counts = counts / area
        norm_counts_error = counts_error / area

        inital_guess = [0.1, 16]
        parameters, covvariance = curve_fit(poisson_f, bin_centers, norm_counts, p0=inital_guess)

        # x = np.linspace(bin_centers.min(), bin_centers.max(), 100)
        x = bin_centers
        self.ax.step(x, poisson_f(x, *parameters), where='mid', color='r', label='Fit')

        self.ax.text(1-.025, .725, f'Risultati del fit $N = {parameters[0]:.2g}$, $\\lambda = {parameters[1]:.2g}$',
                     transform=self.ax.transAxes, ha='right')
        self.ax.text(1-.025, .65, r'Fit = $N\cdot Poisson(x, \lambda) = N\cdot \frac{\lambda^xe^{-\lambda}}{x!}$',
                     transform=self.ax.transAxes, ha='right')

    def __routine__(self, fake):
        if fake:
            x = np.arange(1, 16, 1)
            data = np.random.poisson(lam=6, size=1000)
            self.hist = np.histogram(data, bins=x.shape[0], range=(x.min()-.5, x.max()+.5), density=False)
        else:
            self.__load_data__()

        print("Procediamo adesso a fare l'analisi!")
        option = input('Scrivi "plot" solo per disegnare, "fit" per eseguire un fit (quit per uscire): ')

        if option == 'quit':
            return
        elif option not in ['plot', 'fit']:
            print(f'Ci deve essere stato un errore, scrivi "plot" oppure "fit", non {self.option}')
            return
        elif option == 'plot':
            self.Plot()
        elif option == 'fit':
            self.Plot()
            self.Fit()
        self.ax.legend(frameon=False)
        self.ax.text(.025, .85, f'Modalità: {self.mode}', transform=self.ax.transAxes)
        self.ax.text(.025, .9, 'Distribuzione Poisson',
                     transform=self.ax.transAxes, fontproperties={'style': 'italic'})


class angle(ICD):

    def __load_data__(self):
        npoints = int(input('Dimmi quanti punti (valori  dell angolo) hai preso: '))
        nmeasures = int(input('Dimmi quante misure hai preso per ogni angolo: '))

        data_X, data_Y = [], []
        err_data_X, err_data_Y = [], []

        print('Ora raccogliamo i dati!')

        err_X = float(input('Dimmi il valore di errore sugli angoli (usa il punto per separare i decimali!): '))

        for i in range(npoints):
            data_X.append(float(input(
                f'Dimmi il valore di x_{i}: '
            )))
            err_data_X.append(err_X)

        for i in range(npoints):
            point_y = float(input(f'Dimmi il valore di y_{i}: '))
            data_Y.append(point_y)
            err_data_Y.append(np.sqrt(point_y/nmeasures))

        self.x = np.array(data_X)
        self.ex = np.array(err_data_X)

        self.y = np.array(data_Y)
        self.ey = np.array(err_data_Y)

    def Plot(self):
        self.__plot_init_routine__()
        self.mode = 'plot'

        self.ax.errorbar(self.x, self.y, self.ey, xerr=self.ex,
                         marker='o', ms=3, ls='', color='k', label='Dati sperimentali')

        self.ax.text(1-.025, .8, f'Punti totali {len(self.x)}', transform=self.ax.transAxes, ha='right')
        self.ax.set_ylabel('Conteggi')
        self.ax.set_xlabel('Angolo $\\theta$ [°]')
        # self.ax.set_ylim(-0.1, 0.3)
        self.ax.set_ylim(-1, self.y.max()*1.5)

    def Fit(self):
        self.mode = 'fit'

        parameters, covariance = curve_fit(angle_distribution, self.x, self.y, p0 = [1, 2], sigma=self.ey)

        x = np.linspace(self.x.min()-5, self.x.max()+5)
        self.ax.plot(x, angle_distribution(x, *parameters), color='r', label='Fit')

        self.ax.text(1-.025, .725, f'Risultati del fit $N \\cdot I_0 = {latex_float(parameters[0])}$, $n = {parameters[1]:.2g}$',
                     transform=self.ax.transAxes, ha='right')
        self.ax.text(1-.025, .65, r'Fit = $I_0\cdot \cos^n\theta$',
                     transform=self.ax.transAxes, ha='right')

    def __routine__(self, fake):
        if fake:
            self.x = np.linspace(10, 70, 5)
            self.y = angle_distribution(self.x, 100, 2.33) * np.random.normal(1, 1)
            self.ey = np.sqrt(self.y) / 5
            self.ex = 1
        else:
            self.__load_data__()

        print("Procediamo adesso a fare l'analisi!")
        option = input('Scrivi "plot" solo per disegnare, "fit" per eseguire un fit (quit per uscire): ')

        if option == 'quit':
            return
        elif option not in ['plot', 'fit']:
            print(f'Ci deve essere stato un errore, scrivi "plot" oppure "fit", non {self.option}')
            return
        elif option == 'plot':
            self.Plot()
        elif option == 'fit':
            self.Plot()
            self.Fit()
        self.ax.legend(frameon=False)
        self.ax.text(.025, .85, f'Modalità: {self.mode}', transform=self.ax.transAxes)
        self.ax.text(.025, .9, 'Distribuzione angolare del flusso',
                     transform=self.ax.transAxes, fontproperties={'style': 'italic'})

